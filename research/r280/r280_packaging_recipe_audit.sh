#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/bc250-research}"
OUT="${2:-$HOME/bc250-r280-packaging-recipe-audit.log}"

R180="$ROOT/r180-load-response-observation"
SRC="$ROOT/r152-psp-boundary-src"
MOD="$ROOT/r274b-native-layout-build-v2/amdgpu.ko.unstripped"

{
echo "=== R280 PACKAGING RECIPE AUDIT (READ-ONLY) ==="
date -Ins

echo
echo "=== R279 /BOOT STATE ==="
df -h /boot
df -B1 /boot
for f in   /boot/initramfs-7.2.3-r141-diagnostic.img   /boot/initramfs-7.2.3-r180-observation.img   /boot/loader/entries/boot-entry-r180-observation.conf   /boot/loader/entries/ostree-1.conf   /boot/loader/entries/ostree-2.conf
do
  if sudo test -e "$f"; then
    echo "PRESENT: $f"
  else
    echo "ABSENT: $f"
  fi
done

echo
echo "=== R274-B MODULE ==="
ls -lh "$MOD"
sha256sum "$MOD"
TMPKO="$(mktemp --suffix=.ko)"
cp -- "$MOD" "$TMPKO"
modinfo "$TMPKO" 2>/dev/null | grep -E '^(vermagic|signer|sig_key|sig_hashalgo|srcversion|license|description):' || true
rm -f "$TMPKO"

echo
echo "=== EXACT HISTORICAL PACKAGING SCRIPTS ==="
for f in   "$R180/pack.sh"   "$R180/install.sh"   "$R180/prepare_live.sh"
do
  echo
  echo "--- $f ---"
  if [[ -f "$f" ]]; then
    sha256sum "$f"
    sed -n '1,260p' "$f"
  else
    echo "MISSING"
  fi
done

echo
echo "=== R180 BUILD/CPIO/DEPMOD LOG HEADERS ==="
for f in   "$R180/full-build.log"   "$R180/cpio.log"   "$R180/depmod.log"
do
  echo
  echo "--- $f ---"
  if [[ -f "$f" ]]; then
    sha256sum "$f"
    sed -n '1,220p' "$f"
  else
    echo "MISSING"
  fi
done

echo
echo "=== SIGNING MATERIAL IDENTITY ==="
for f in   "$SRC/certs/signing_key.pem"   "$SRC/certs/signing_key.x509"   "$SRC/scripts/sign-file"
do
  echo
  echo "--- $f ---"
  if [[ -f "$f" ]]; then
    ls -lh "$f"
    sha256sum "$f"
    file "$f" || true
  else
    echo "MISSING"
  fi
done

echo
echo "=== R180 CERT / SIGNATURE REFERENCES ==="
for f in   "$R180/signature-verification.json"   "$R180/module-notes.txt"   "$R180/SHA256SUMS"   "$R180/full-build-results.json"
do
  echo
  echo "--- $f ---"
  if [[ -f "$f" ]]; then
    sed -n '1,240p' "$f"
  else
    echo "MISSING"
  fi
done

echo
echo "=== MODULE ROOT / FIRMWARE INPUTS ==="
for p in   "$ROOT/r137-modules-root/lib/modules/7.2.3+"   "$ROOT/r137-modules-root/lib/firmware"   "$ROOT/r136-boot-artifact/vcn_2_0_3.bin"
do
  if [[ -e "$p" ]]; then
    echo "PRESENT: $p"
    if [[ -f "$p" ]]; then sha256sum "$p"; fi
  else
    echo "MISSING: $p"
  fi
done

echo
echo "=== TOOL AVAILABILITY ==="
for t in dracut depmod modinfo strip objcopy cpio gzip lsinitrd openssl; do
  if command -v "$t" >/dev/null 2>&1; then
    echo "$t=$(command -v "$t")"
  else
    echo "$t=ABSENT"
  fi
done

echo
echo "R280_READ_ONLY=YES"
echo "NO_MODULE_MODIFIED=YES"
echo "NO_INITRAMFS_CREATED=YES"
echo "NO_BOOT_CHANGED=YES"
echo "NO_REBOOT=YES"
} 2>&1 | tee "$OUT"

echo
echo "WROTE=$OUT"
sha256sum "$OUT"
