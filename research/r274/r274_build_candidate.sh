#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/bc250-research/r152-psp-boundary-src}"
OUTDIR="${2:-$HOME/bc250-research/r274-minimal-direct-load-build}"
AMD="$ROOT/drivers/gpu/drm/amd/amdgpu"
SRC="$AMD/amdgpu_vcn.c"
EXPECTED="09d8076366f028a1e6cf416c3989147a35ad488fb1a8e311490e345109d8d099"

mkdir -p "$OUTDIR"
LOG="$OUTDIR/build.log"
PATCH="$OUTDIR/r274-minimal-direct-load.patch"
BASE="$OUTDIR/amdgpu_vcn.c.baseline"
CAND="$OUTDIR/amdgpu_vcn.c.candidate"

if [[ ! -f "$SRC" ]]; then
  echo "STOP: missing $SRC" >&2
  exit 2
fi

ACTUAL="$(sha256sum "$SRC" | awk '{print $1}')"
if [[ "$ACTUAL" != "$EXPECTED" ]]; then
  echo "STOP: source identity mismatch" >&2
  echo "expected=$EXPECTED" >&2
  echo "actual=$ACTUAL" >&2
  exit 3
fi

cp -- "$SRC" "$BASE"

restore() {
  if [[ -f "$BASE" ]]; then
    cp -- "$BASE" "$SRC"
  fi
}
trap restore EXIT INT TERM

python3 - "$BASE" "$CAND" <<'PY'
from pathlib import Path
import sys

src = Path(sys.argv[1]).read_text()
out = Path(sys.argv[2])

if '#include <linux/slab.h>\n' not in src:
    anchor = '#include <linux/module.h>\n'
    if anchor not in src:
        raise SystemExit("missing slab include anchor")
    src = src.replace(anchor, anchor + '#include <linux/slab.h>\n', 1)

if '"amdgpu_uvd.h"' not in src:
    anchor = '#include "amdgpu_vcn.h"\n'
    if anchor not in src:
        raise SystemExit("missing include anchor")
    src = src.replace(anchor, anchor + '#include "amdgpu_uvd.h"\n', 1)

old = '''	bo_size = AMDGPU_VCN_STACK_SIZE + AMDGPU_VCN_CONTEXT_SIZE;
	if (adev->firmware.load_type != AMDGPU_FW_LOAD_PSP)
		bo_size += AMDGPU_GPU_PAGE_ALIGN(le32_to_cpu(hdr->ucode_size_bytes) + 8);
'''
new = '''	bo_size = AMDGPU_VCN_STACK_SIZE + AMDGPU_VCN_CONTEXT_SIZE;
	if ((adev->asic_type == CHIP_CYAN_SKILLFISH &&
	     amdgpu_ip_version(adev, UVD_HWIP, 0) == IP_VERSION(2, 0, 3)) ||
	    adev->firmware.load_type != AMDGPU_FW_LOAD_PSP)
		bo_size += AMDGPU_GPU_PAGE_ALIGN(le32_to_cpu(hdr->ucode_size_bytes) + 8);
'''
if src.count(old) != 1:
    raise SystemExit(f"bo_size anchor count={src.count(old)}")
src = src.replace(old, new, 1)

old = '''	} else {
		const struct common_firmware_header *hdr;
		unsigned int offset;

		hdr = (const struct common_firmware_header *)adev->vcn.inst[i].fw->data;
		if (adev->firmware.load_type != AMDGPU_FW_LOAD_PSP) {
			offset = le32_to_cpu(hdr->ucode_array_offset_bytes);
			if (drm_dev_enter(adev_to_drm(adev), &idx)) {
				memcpy_toio(adev->vcn.inst[i].cpu_addr,
					    adev->vcn.inst[i].fw->data + offset,
					    le32_to_cpu(hdr->ucode_size_bytes));
				drm_dev_exit(idx);
			}
			size -= le32_to_cpu(hdr->ucode_size_bytes);
			ptr += le32_to_cpu(hdr->ucode_size_bytes);
		}
		memset_io(ptr, 0, size);
	}
'''
new = '''	} else {
		const struct common_firmware_header *hdr;
		unsigned int offset;

		hdr = (const struct common_firmware_header *)adev->vcn.inst[i].fw->data;
		if (adev->asic_type == CHIP_CYAN_SKILLFISH &&
		    amdgpu_ip_version(adev, UVD_HWIP, 0) == IP_VERSION(2, 0, 3)) {
			unsigned int ucode_bytes = le32_to_cpu(hdr->ucode_size_bytes);
			unsigned int dst_offset = AMDGPU_UVD_FIRMWARE_OFFSET;
			void *verify;
			bool equal;

			offset = le32_to_cpu(hdr->ucode_array_offset_bytes);
			if (dst_offset > size || ucode_bytes > size - dst_offset) {
				dev_err(adev->dev,
					"BC250 R274 direct_copy: bounds_fail bo=%u dst=%u bytes=%u\\n",
					size, dst_offset, ucode_bytes);
				return -EINVAL;
			}

			verify = kvmalloc(ucode_bytes, GFP_KERNEL);
			if (!verify)
				return -ENOMEM;

			if (!drm_dev_enter(adev_to_drm(adev), &idx)) {
				kvfree(verify);
				return -ENODEV;
			}

			memset_io(ptr, 0, size);
			memcpy_toio((u8 *)ptr + dst_offset,
				    adev->vcn.inst[i].fw->data + offset,
				    ucode_bytes);
			memcpy_fromio(verify, (u8 *)ptr + dst_offset, ucode_bytes);
			drm_dev_exit(idx);

			equal = !memcmp(verify,
					adev->vcn.inst[i].fw->data + offset,
					ucode_bytes);
			kvfree(verify);

			dev_info(adev->dev,
				 "BC250 R274 direct_copy: bytes=%u src_off=%u dst_off=%u bo=%u equal=%u\\n",
				 ucode_bytes, offset, dst_offset, size, equal ? 1 : 0);
			if (!equal)
				return -EIO;
		} else if (adev->firmware.load_type != AMDGPU_FW_LOAD_PSP) {
			offset = le32_to_cpu(hdr->ucode_array_offset_bytes);
			if (drm_dev_enter(adev_to_drm(adev), &idx)) {
				memcpy_toio(adev->vcn.inst[i].cpu_addr,
					    adev->vcn.inst[i].fw->data + offset,
					    le32_to_cpu(hdr->ucode_size_bytes));
				drm_dev_exit(idx);
			}
			size -= le32_to_cpu(hdr->ucode_size_bytes);
			ptr += le32_to_cpu(hdr->ucode_size_bytes);
			memset_io(ptr, 0, size);
		} else {
			memset_io(ptr, 0, size);
		}
	}
'''
if src.count(old) != 1:
    raise SystemExit(f"resume anchor count={src.count(old)}")
src = src.replace(old, new, 1)

out.write_text(src)
PY

diff -u --label a/drivers/gpu/drm/amd/amdgpu/amdgpu_vcn.c         --label b/drivers/gpu/drm/amd/amdgpu/amdgpu_vcn.c         "$BASE" "$CAND" >"$PATCH" || test $? -eq 1

cp -- "$CAND" "$SRC"

{
  echo "=== R274 SOURCE-ONLY CANDIDATE BUILD ==="
  date -Ins
  echo "ROOT=$ROOT"
  echo "BASELINE_SHA256=$EXPECTED"
  echo "CANDIDATE_SHA256=$(sha256sum "$SRC" | awk '{print $1}')"
  echo
  echo "=== PATCH ==="
  cat "$PATCH"
  echo
  echo "=== KBUILD ==="
  make -C "$ROOT" -j8 M=drivers/gpu/drm/amd/amdgpu modules
  echo
  echo "=== OUTPUT MODULE ==="
  ls -lh "$AMD/amdgpu.ko"
  sha256sum "$AMD/amdgpu.ko"
} 2>&1 | tee "$LOG"

cp -- "$AMD/amdgpu.ko" "$OUTDIR/amdgpu.ko.unstripped"
sha256sum "$OUTDIR/amdgpu.ko.unstripped" >"$OUTDIR/amdgpu.ko.unstripped.sha256"

restore
trap - EXIT INT TERM

RESTORED="$(sha256sum "$SRC" | awk '{print $1}')"
echo "RESTORED_SOURCE_SHA256=$RESTORED" | tee -a "$LOG"
if [[ "$RESTORED" != "$EXPECTED" ]]; then
  echo "STOP: source restoration hash mismatch" >&2
  exit 4
fi

echo "R274_BUILD_ONLY_COMPLETE=YES"
echo "NO_MODULE_INSTALLED=YES"
echo "NO_BOOT_ARTIFACT_CHANGED=YES"
echo "OUTDIR=$OUTDIR"
