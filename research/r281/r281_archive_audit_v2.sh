#!/usr/bin/env bash
set -euo pipefail
export LC_ALL=C

ROOT="${1:-$HOME/bc250-research}"
D="${2:-$ROOT/r281-r274b-home-initramfs}"
OUT="${3:-$HOME/bc250-r281-archive-audit-v2.log}"

IMAGE="$D/initramfs-7.2.3-r281-r274b.img"
TREE="$D/initramfs-tree"

MODULE_REL="usr/lib/modules/7.2.3+/kernel/drivers/gpu/drm/amd/amdgpu/amdgpu.ko"
FW_REL="usr/lib/firmware/amdgpu/vcn_2_0_3.bin"

EXPECTED_IMAGE="9765259d44bc1719c24318f3ac970fbbf74272b17e854aefb2b8380f12e7099c"
EXPECTED_MODULE="56bdac20c742ebb87844782bd1ee608e6b679095feae244f0eede4a18bd45f41"
EXPECTED_FW="a9ec155695b5020009d3986cfd4ebd00ad9ddbd12ac7e5fa15ec86b8a571dbe5"

fail() { echo "STOP: $*" >&2; exit 1; }

[[ -f "$IMAGE" ]] || fail "missing image: $IMAGE"
[[ -f "$TREE/$MODULE_REL" ]] || fail "missing tree module"
[[ -f "$TREE/$FW_REL" ]] || fail "missing tree firmware"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
LIST="$TMP/archive.list"

{
echo "=== R281 ARCHIVE AUDIT V2 ==="
date -Ins

echo
echo "=== IMAGE IDENTITY ==="
IMAGE_SHA="$(sha256sum "$IMAGE" | awk '{print $1}')"
IMAGE_SIZE="$(stat -c '%s' "$IMAGE")"
echo "IMAGE_SIZE=$IMAGE_SIZE"
echo "IMAGE_SHA256=$IMAGE_SHA"
[[ "$IMAGE_SHA" == "$EXPECTED_IMAGE" ]] || fail "image hash mismatch"

echo
echo "=== TREE IDENTITIES ==="
TREE_MOD_SHA="$(sha256sum "$TREE/$MODULE_REL" | awk '{print $1}')"
TREE_FW_SHA="$(sha256sum "$TREE/$FW_REL" | awk '{print $1}')"
echo "TREE_MODULE_SHA256=$TREE_MOD_SHA"
echo "TREE_FW_SHA256=$TREE_FW_SHA"
[[ "$TREE_MOD_SHA" == "$EXPECTED_MODULE" ]] || fail "tree module hash mismatch"
[[ "$TREE_FW_SHA" == "$EXPECTED_FW" ]] || fail "tree firmware hash mismatch"

echo
echo "=== ACTUAL CPIO MEMBER NAMES ==="
gzip -dc "$IMAGE" | cpio -it --quiet > "$LIST"
MOD_MEMBER="$(grep -E '(^|/)usr/lib/modules/7\.2\.3\+/kernel/drivers/gpu/drm/amd/amdgpu/amdgpu\.ko$' "$LIST" | head -1 || true)"
FW_MEMBER="$(grep -E '(^|/)usr/lib/firmware/amdgpu/vcn_2_0_3\.bin$' "$LIST" | head -1 || true)"
echo "MODULE_MEMBER=$MOD_MEMBER"
echo "FW_MEMBER=$FW_MEMBER"
[[ -n "$MOD_MEMBER" ]] || fail "module member not found in archive listing"
[[ -n "$FW_MEMBER" ]] || fail "firmware member not found in archive listing"

echo
echo "=== TARGETED EXTRACTION ==="
(
  cd "$TMP"
  gzip -dc "$IMAGE" | cpio -id --quiet --no-absolute-filenames "$MOD_MEMBER" "$FW_MEMBER"
)

MOD_PATH="$TMP/${MOD_MEMBER#./}"
FW_PATH="$TMP/${FW_MEMBER#./}"
[[ -f "$MOD_PATH" ]] || fail "extracted module missing"
[[ -f "$FW_PATH" ]] || fail "extracted firmware missing"

ARCHIVE_MOD_SHA="$(sha256sum "$MOD_PATH" | awk '{print $1}')"
ARCHIVE_FW_SHA="$(sha256sum "$FW_PATH" | awk '{print $1}')"
echo "ARCHIVE_MODULE_SHA256=$ARCHIVE_MOD_SHA"
echo "ARCHIVE_FW_SHA256=$ARCHIVE_FW_SHA"

[[ "$ARCHIVE_MOD_SHA" == "$EXPECTED_MODULE" ]] || fail "archive module hash mismatch"
[[ "$ARCHIVE_FW_SHA" == "$EXPECTED_FW" ]] || fail "archive firmware hash mismatch"

echo
echo "=== EXTRACTED MODULE METADATA ==="
modinfo "$MOD_PATH" | grep -E '^(filename|license|description|author|version|srcversion|vermagic|signer|sig_key|sig_hashalgo):' || true

for m in   "BC250 R141 psp_vcn_enrollment: skipped (R79 guard)"   "BC250 R141 vcn_hw_init: skipped"   "BC250 R274B direct_copy:"
do
  grep -aFq "$m" "$MOD_PATH" || fail "required marker missing in archive module: $m"
  echo "PRESENT: $m"
done

if grep -aFq "BC250 R274 direct_copy:" "$MOD_PATH"; then
  fail "old R274-A marker present in archive module"
fi
echo "R274A_MARKER_PRESENT=NO"

echo
echo "=== /BOOT STATE (READ ONLY) ==="
df -B1 /boot
for f in   /boot/initramfs-7.2.3-r180-observation.img   /boot/loader/entries/boot-entry-r180-observation.conf   /boot/loader/entries/ostree-1.conf   /boot/loader/entries/ostree-2.conf
do
  if sudo test -e "$f"; then
    echo "PRESENT: $f"
  else
    fail "recovery file missing: $f"
  fi
done

echo
echo "R281_ARCHIVE_AUDIT_V2=PASS"
echo "ARCHIVE_MODULE_EQUALS_TREE=YES"
echo "ARCHIVE_FW_EQUALS_EXPECTED=YES"
echo "NO_IMAGE_REBUILD=YES"
echo "NO_BOOT_WRITE=YES"
echo "NO_MODULE_LOAD=YES"
echo "NO_REBOOT=YES"
} 2>&1 | tee "$OUT"

echo
echo "WROTE=$OUT"
sha256sum "$OUT"
