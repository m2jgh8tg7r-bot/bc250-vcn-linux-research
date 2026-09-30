#!/usr/bin/env bash
set -euo pipefail
export LC_ALL=C

ROOT="${1:-$HOME/bc250-research}"
OUTDIR="${2:-$ROOT/r281-r274b-home-initramfs}"
LOG="${3:-$HOME/bc250-r281-home-initramfs.log}"

BASE_TREE="$ROOT/r180-load-response-observation/initramfs-tree"
SRC="$ROOT/r152-psp-boundary-src"
UNSTRIPPED="$ROOT/r274b-native-layout-build-v2/amdgpu.ko.unstripped"
FW="$ROOT/r136-boot-artifact/vcn_2_0_3.bin"

EXPECTED_MOD="b1138dd396c0a0e31b3431b9da1a50ae1f564a0ef102864e63e4a75763576ef5"
EXPECTED_BASE_R180_MOD="5185df438a65ae63cd4619e10e4ead2fd8fe8483538743d81b7acdb48c8de78a"
EXPECTED_KEY="904b7b14a8fbd11de3f73e699ecfa3c1a95da3616915fe4ed490049f559a6f4c"
EXPECTED_CERT="6f425bc02a1f554b7169d61ad8f6d22ab691981829f7cb59a05e1201c1a4e92f"
EXPECTED_SIGNFILE="36264b18a597d20c0235be6a233ba13be3428e7fc50f2a26287e11a97c83d62b"
EXPECTED_FW="a9ec155695b5020009d3986cfd4ebd00ad9ddbd12ac7e5fa15ec86b8a571dbe5"

KEY="$SRC/certs/signing_key.pem"
CERT="$SRC/certs/signing_key.x509"
SIGNFILE="$SRC/scripts/sign-file"
MODULE_REL="usr/lib/modules/7.2.3+/kernel/drivers/gpu/drm/amd/amdgpu/amdgpu.ko"
FW_REL="usr/lib/firmware/amdgpu/vcn_2_0_3.bin"

fail() { echo "STOP: $*" >&2; exit 1; }

[[ ! -e "$OUTDIR" ]] || fail "OUTDIR already exists: $OUTDIR"
mkdir -p "$OUTDIR"

{
echo "=== R281 HOME-ONLY R274-B INITRAMFS BUILD ==="
date -Ins

echo
echo "=== INPUT IDENTITY ==="
for spec in   "$UNSTRIPPED:$EXPECTED_MOD"   "$KEY:$EXPECTED_KEY"   "$CERT:$EXPECTED_CERT"   "$SIGNFILE:$EXPECTED_SIGNFILE"   "$FW:$EXPECTED_FW"
do
  f="${spec%%:*}"
  exp="${spec##*:}"
  [[ -f "$f" ]] || fail "missing input: $f"
  got="$(sha256sum "$f" | awk '{print $1}')"
  echo "$f"
  echo " expected=$exp"
  echo " actual=$got"
  [[ "$got" == "$exp" ]] || fail "input hash mismatch: $f"
done

echo
echo "=== BASE TREE IDENTITY ==="
[[ -d "$BASE_TREE" ]] || fail "missing R180 initramfs tree"
BASE_MOD="$BASE_TREE/$MODULE_REL"
BASE_FW="$BASE_TREE/$FW_REL"
[[ -f "$BASE_MOD" ]] || fail "missing R180 tree amdgpu module"
[[ -f "$BASE_FW" ]] || fail "missing R180 tree VCN firmware"
BASE_MOD_SHA="$(sha256sum "$BASE_MOD" | awk '{print $1}')"
BASE_FW_SHA="$(sha256sum "$BASE_FW" | awk '{print $1}')"
echo "BASE_R180_MODULE_SHA256=$BASE_MOD_SHA"
echo "BASE_FW_SHA256=$BASE_FW_SHA"
[[ "$BASE_MOD_SHA" == "$EXPECTED_BASE_R180_MOD" ]] || fail "R180 tree module identity mismatch"
[[ "$BASE_FW_SHA" == "$EXPECTED_FW" ]] || fail "R180 tree firmware identity mismatch"

echo
echo "=== CLONE TREE ==="
cp -a -- "$BASE_TREE" "$OUTDIR/initramfs-tree"
TREE="$OUTDIR/initramfs-tree"
MODULE="$TREE/$MODULE_REL"
IMAGE="$OUTDIR/initramfs-7.2.3-r281-r274b.img"
DEPMOD_LOG="$OUTDIR/depmod.log"
CPIO_LOG="$OUTDIR/cpio.log"

echo "TREE=$TREE"
echo "IMAGE=$IMAGE"

echo
echo "=== REPLACE MODULE / STRIP / SIGN ==="
install -m 0644 "$UNSTRIPPED" "$MODULE"
echo "UNSTRIPPED_INSTALLED_SHA256=$(sha256sum "$MODULE" | awk '{print $1}')"
strip --strip-debug "$MODULE"
STRIPPED_SHA="$(sha256sum "$MODULE" | awk '{print $1}')"
STRIPPED_SIZE="$(stat -c '%s' "$MODULE")"
echo "STRIPPED_SIZE=$STRIPPED_SIZE"
echo "STRIPPED_SHA256=$STRIPPED_SHA"

"$SIGNFILE" sha512 "$KEY" "$CERT" "$MODULE"
SIGNED_SHA="$(sha256sum "$MODULE" | awk '{print $1}')"
SIGNED_SIZE="$(stat -c '%s' "$MODULE")"
echo "SIGNED_SIZE=$SIGNED_SIZE"
echo "SIGNED_SHA256=$SIGNED_SHA"

echo
echo "=== SIGNED MODULE METADATA ==="
modinfo "$MODULE" | grep -E '^(filename|license|description|author|version|srcversion|vermagic|signer|sig_key|sig_hashalgo):' || true
VERMAGIC="$(modinfo -F vermagic "$MODULE" 2>/dev/null || true)"
[[ "$VERMAGIC" == "7.2.3+ SMP preempt mod_unload " ]] || fail "unexpected vermagic: $VERMAGIC"

for m in   "BC250 R141 psp_vcn_enrollment: skipped (R79 guard)"   "BC250 R141 vcn_hw_init: skipped"   "BC250 R274B direct_copy:"
do
  grep -aFq "$m" "$MODULE" || fail "required marker missing after strip/sign: $m"
  echo "PRESENT: $m"
done
if grep -aFq "BC250 R274 direct_copy:" "$MODULE"; then
  fail "old R274-A marker present"
fi
echo "R274A_MARKER_PRESENT=NO"

echo
echo "=== DEPMOD ==="
depmod -b "$TREE" -e -E "$SRC/Module.symvers" 7.2.3+ >"$DEPMOD_LOG" 2>&1
if [[ -s "$DEPMOD_LOG" ]]; then
  cat "$DEPMOD_LOG"
  fail "depmod produced diagnostics"
fi
echo "DEPMOD_LOG_EMPTY=YES"

echo
echo "=== CPIO/GZIP ==="
(
  cd "$TREE"
  find . -print0 | LC_ALL=C sort -z |     cpio --null -o --format=newc --owner=0:0 2>"$CPIO_LOG" |     gzip -1 >"$IMAGE.tmp"
)
mv "$IMAGE.tmp" "$IMAGE"
ls -lh "$IMAGE"
IMAGE_SHA="$(sha256sum "$IMAGE" | awk '{print $1}')"
IMAGE_SIZE="$(stat -c '%s' "$IMAGE")"
echo "IMAGE_SIZE=$IMAGE_SIZE"
echo "IMAGE_SHA256=$IMAGE_SHA"

echo
echo "=== ARCHIVE BYTE VERIFICATION ==="
TREE_MOD_SHA="$(sha256sum "$MODULE" | awk '{print $1}')"
ARCHIVE_MOD_SHA="$(
  gzip -dc "$IMAGE" | cpio -i --quiet --to-stdout "./$MODULE_REL" | sha256sum | awk '{print $1}'
)"
TREE_FW_SHA="$(sha256sum "$TREE/$FW_REL" | awk '{print $1}')"
ARCHIVE_FW_SHA="$(
  gzip -dc "$IMAGE" | cpio -i --quiet --to-stdout "./$FW_REL" | sha256sum | awk '{print $1}'
)"
echo "TREE_MODULE_SHA256=$TREE_MOD_SHA"
echo "ARCHIVE_MODULE_SHA256=$ARCHIVE_MOD_SHA"
echo "TREE_FW_SHA256=$TREE_FW_SHA"
echo "ARCHIVE_FW_SHA256=$ARCHIVE_FW_SHA"
[[ "$ARCHIVE_MOD_SHA" == "$TREE_MOD_SHA" ]] || fail "archive module differs from tree"
[[ "$ARCHIVE_FW_SHA" == "$EXPECTED_FW" ]] || fail "archive firmware mismatch"
[[ "$TREE_FW_SHA" == "$EXPECTED_FW" ]] || fail "tree firmware mismatch"

echo
echo "=== ARCHIVE LISTING TARGETS ==="
lsinitrd "$IMAGE" 2>/dev/null | grep -E 'amdgpu\.ko$|vcn_2_0_3\.bin$' || true

echo
echo "=== /BOOT UNTOUCHED CHECK ==="
df -B1 /boot
echo "R281_HOME_ONLY_BUILD=PASS"
echo "NO_BOOT_WRITE=YES"
echo "NO_MODULE_LOAD=YES"
echo "NO_REBOOT=YES"
} 2>&1 | tee "$LOG"

echo
echo "WROTE=$LOG"
sha256sum "$LOG"
