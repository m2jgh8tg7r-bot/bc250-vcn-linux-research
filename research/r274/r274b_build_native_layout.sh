#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/bc250-research/r152-psp-boundary-src}"
OUTDIR="${2:-$HOME/bc250-research/r274b-native-layout-build}"
AMD="$ROOT/drivers/gpu/drm/amd/amdgpu"
SRC="$AMD/amdgpu_vcn.c"

declare -A EXPECTED
EXPECTED[amdgpu_vcn.c]="09d8076366f028a1e6cf416c3989147a35ad488fb1a8e311490e345109d8d099"
EXPECTED[amdgpu_psp.c]="2087292def28e46fec9f4df25b152429eabb411e7be748e4121b7232f9f753a2"
EXPECTED[vcn_v2_0.c]="eb62b3f8575eff45019712ebc3f68acf4d190834900eb591b5ff7416a42ff075"
EXPECTED[amdgpu_discovery.c]="37202992e43a0d450b0b7e0d9c1e47ca97af95f8d1d02e6f22108aaf9d5302b5"
EXPECTED[amdgpu_device.c]="cc9fe304c5e51434bb7a2bc4e04ecd3ce61c95e642ea2e9e8ec910d6eb66b679"

mkdir -p "$OUTDIR"
LOG="$OUTDIR/build.log"
PATCH="$OUTDIR/r274b-native-layout.patch"
BASE="$OUTDIR/amdgpu_vcn.c.baseline"
CAND="$OUTDIR/amdgpu_vcn.c.candidate"

echo "=== SOURCE IDENTITY PREFLIGHT ===" | tee "$LOG"
for f in amdgpu_vcn.c amdgpu_psp.c vcn_v2_0.c amdgpu_discovery.c amdgpu_device.c; do
  path="$AMD/$f"
  if [[ ! -f "$path" ]]; then
    echo "STOP: missing $path" | tee -a "$LOG" >&2
    exit 2
  fi
  actual="$(sha256sum "$path" | awk '{print $1}')"
  echo "$f expected=${EXPECTED[$f]} actual=$actual" | tee -a "$LOG"
  if [[ "$actual" != "${EXPECTED[$f]}" ]]; then
    echo "STOP: source identity mismatch: $f" | tee -a "$LOG" >&2
    exit 3
  fi
done

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
			size_t fw_size = adev->vcn.inst[i].fw->size;
			void *verify;
			bool equal;

			offset = le32_to_cpu(hdr->ucode_array_offset_bytes);

			if (offset > fw_size || ucode_bytes > fw_size - offset) {
				dev_err(adev->dev,
					"BC250 R274B direct_copy: source_bounds_fail fw=%zu src=%u bytes=%u\\n",
					fw_size, offset, ucode_bytes);
				return -EINVAL;
			}
			if (ucode_bytes > size) {
				dev_err(adev->dev,
					"BC250 R274B direct_copy: bo_bounds_fail bo=%u bytes=%u\\n",
					size, ucode_bytes);
				return -EINVAL;
			}

			verify = kvmalloc(ucode_bytes, GFP_KERNEL);
			if (!verify)
				return -ENOMEM;

			if (!drm_dev_enter(adev_to_drm(adev), &idx)) {
				kvfree(verify);
				return -ENODEV;
			}

			/* Match the native non-PSP VCN layout: ucode begins at BO offset 0. */
			memcpy_toio(ptr,
				    adev->vcn.inst[i].fw->data + offset,
				    ucode_bytes);
			if (size > ucode_bytes)
				memset_io((u8 *)ptr + ucode_bytes, 0, size - ucode_bytes);
			memcpy_fromio(verify, ptr, ucode_bytes);
			drm_dev_exit(idx);

			equal = !memcmp(verify,
					adev->vcn.inst[i].fw->data + offset,
					ucode_bytes);
			kvfree(verify);

			dev_info(adev->dev,
				 "BC250 R274B direct_copy: bytes=%u src_off=%u dst_off=0 bo=%u equal=%u\\n",
				 ucode_bytes, offset, size, equal ? 1 : 0);
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
  echo
  echo "=== R274-B NATIVE-LAYOUT BUILD ==="
  date -Ins
  echo "ROOT=$ROOT"
  echo "BASELINE_VCN_SHA256=${EXPECTED[amdgpu_vcn.c]}"
  echo "CANDIDATE_VCN_SHA256=$(sha256sum "$SRC" | awk '{print $1}')"
  echo
  echo "=== PATCH ==="
  cat "$PATCH"
  echo
  echo "=== ADDED CONTROL-TOKEN CHECK ==="
  if grep '^+' "$PATCH" | grep -Ev '^\+\+\+' | grep -E 'WREG|RREG|SMN|vcn_v2_0_start|amdgpu_ring_init|LOAD_IP_FW|psp_cmd|doorbell|soft_reset'; then
    echo "STOP: added hardware-control token detected"
    exit 5
  else
    echo "ADDED_HARDWARE_CONTROL_TOKENS=NONE"
  fi
  echo
  echo "=== KBUILD ==="
  make -C "$ROOT" -j8 M=drivers/gpu/drm/amd/amdgpu modules
  echo
  echo "=== OUTPUT MODULE ==="
  ls -lh "$AMD/amdgpu.ko"
  sha256sum "$AMD/amdgpu.ko"
} 2>&1 | tee -a "$LOG"

cp -- "$AMD/amdgpu.ko" "$OUTDIR/amdgpu.ko.unstripped"
sha256sum "$OUTDIR/amdgpu.ko.unstripped" >"$OUTDIR/amdgpu.ko.unstripped.sha256"

restore
trap - EXIT INT TERM

RESTORED="$(sha256sum "$SRC" | awk '{print $1}')"
echo "RESTORED_SOURCE_SHA256=$RESTORED" | tee -a "$LOG"
if [[ "$RESTORED" != "${EXPECTED[amdgpu_vcn.c]}" ]]; then
  echo "STOP: source restoration hash mismatch" >&2
  exit 6
fi

echo "R274B_BUILD_ONLY_COMPLETE=YES"
echo "NO_MODULE_INSTALLED=YES"
echo "NO_BOOT_ARTIFACT_CHANGED=YES"
echo "OUTDIR=$OUTDIR"
