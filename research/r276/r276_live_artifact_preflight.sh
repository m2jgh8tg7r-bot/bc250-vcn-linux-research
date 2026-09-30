#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/bc250-research}"
OUT="${2:-$HOME/bc250-r276-live-artifact-preflight.log}"
MOD="$ROOT/r274b-native-layout-build-v2/amdgpu.ko.unstripped"

{
echo "=== R276 LIVE-ARTIFACT PREFLIGHT (READ-ONLY) ==="
date -Ins

echo
echo "=== CURRENT RUNNING KERNEL ==="
uname -a
uname -r

echo
echo "=== R274-B MODULE ==="
if [[ -f "$MOD" ]]; then
  ls -lh "$MOD"
  sha256sum "$MOD"
  TMPKO="$(mktemp --suffix=.ko)"
  cp -- "$MOD" "$TMPKO"
  modinfo "$TMPKO" 2>/dev/null | grep -E '^(license|description|author|version|srcversion|vermagic|signer|sig_key|sig_hashalgo):' || true
  rm -f "$TMPKO"
else
  echo "MISSING: $MOD"
fi

echo
echo "=== RETAINED 7.2.3 KERNEL CANDIDATES ==="
for f in   /boot/vmlinuz-7.2.3-r138   /boot/vmlinuz-7.2.3-ogc-r135.bzImage   "$ROOT/r138-boot-repair/vmlinuz-7.2.3-r138"   "$ROOT/r136-boot-artifact/vmlinuz-7.2.3-ogc-r135.bzImage"
do
  if [[ -f "$f" ]]; then
    ls -lh "$f"
    sha256sum "$f"
  else
    echo "MISSING: $f"
  fi
done

echo
echo "=== RETAINED R180 INITRAMFS CANDIDATES ==="
for f in   /boot/initramfs-7.2.3-r180-observation.img   "$ROOT/r180-load-response-observation/initramfs-7.2.3-r180-observation.img"
do
  if [[ -f "$f" ]]; then
    ls -lh "$f"
    sha256sum "$f"
  else
    echo "MISSING: $f"
  fi
done

echo
echo "=== BOOT ENTRY INVENTORY ==="
for d in /boot/loader/entries /boot/efi/loader/entries; do
  if [[ -d "$d" ]]; then
    echo "--- $d ---"
    find "$d" -maxdepth 1 -type f -print | sort
    echo
    grep -H -E '^(title|version|linux|initrd|options) ' "$d"/* 2>/dev/null |       grep -E 'R180|R173|7\.2\.3|bazzite|Bazzite' || true
  fi
done

echo
echo "=== /BOOT SPACE ==="
df -h /boot 2>/dev/null || true
df -h /boot/efi 2>/dev/null || true

echo
echo "=== HISTORICAL R180 LOCAL ENTRY FILE ==="
for f in   "$ROOT/r180-load-response-observation/boot-entry-r180-observation.conf"   "$ROOT/r173-request-observation/boot-entry-r173-observation.conf"
do
  if [[ -f "$f" ]]; then
    echo "--- $f ---"
    sha256sum "$f"
    sed -n '1,30p' "$f"
  else
    echo "MISSING: $f"
  fi
done

echo
echo "=== SIGNING / PACKAGE INPUT INVENTORY ==="
find "$ROOT" -maxdepth 3 -type f \(   -name '*.pem' -o -name '*.x509' -o -name '*.der' -o   -name '*sign*.key' -o -name '*sign*.pem' -o   -name 'pack.sh' -o -name 'install.sh' -o -name 'prepare_live.sh' \) -print 2>/dev/null | sort | head -200

echo
echo "=== SOURCE BASELINE ==="
AMD="$ROOT/r152-psp-boundary-src/drivers/gpu/drm/amd/amdgpu"
for f in amdgpu_vcn.c amdgpu_psp.c vcn_v2_0.c amdgpu_discovery.c amdgpu_device.c; do
  if [[ -f "$AMD/$f" ]]; then
    sha256sum "$AMD/$f"
  else
    echo "MISSING: $AMD/$f"
  fi
done

echo
echo "=== EXPECTED HISTORICAL IDENTITIES ==="
echo "kernel_expected=c556be76b14b42edf41b6d4d3b6526f41daf694fa79348da9c0d0231e02bb6c6"
echo "r180_initramfs_expected=b6ef569b85e24a5dedc81b076e4d4f977538bde400fb31c7d13d0674bb84c007"
echo "r274b_module_expected=b1138dd396c0a0e31b3431b9da1a50ae1f564a0ef102864e63e4a75763576ef5"

echo
echo "=== R276 PREFLIGHT END ==="
} 2>&1 | tee "$OUT"

echo
echo "WROTE=$OUT"
sha256sum "$OUT"
