#!/usr/bin/env bash
set -euo pipefail
OUT="${1:-$HOME/bc250-r277-boot-space-inventory.log}"

{
echo "=== R277 /BOOT SPACE INVENTORY (READ-ONLY) ==="
date -Ins

echo
echo "=== FILESYSTEM ==="
df -h /boot /boot/efi 2>/dev/null || true
df -B1 /boot 2>/dev/null || true

echo
echo "=== /BOOT TOP LEVEL, SIZE SORTED ==="
find /boot -maxdepth 1 -type f -printf '%s\t%M\t%u:%g\t%TY-%Tm-%Td %TH:%TM\t%p\n' 2>/dev/null | sort -nr

echo
echo "=== /BOOT DIRECTORIES ==="
du -x -B1 -d1 /boot 2>/dev/null | sort -nr || true

echo
echo "=== BLS ENTRY REFERENCES ==="
for d in /boot/loader/entries /boot/efi/loader/entries; do
  if [[ -d "$d" ]]; then
    echo "--- $d ---"
    for f in "$d"/*; do
      [[ -f "$f" ]] || continue
      echo "### $f"
      grep -E '^(title|version|linux|initrd|efi|options) ' "$f" 2>/dev/null || true
    done
  fi
done

echo
echo "=== LARGE /BOOT FILES >= 32 MiB ==="
find /boot -xdev -type f -size +32M -printf '%s\t%M\t%u:%g\t%p\n' 2>/dev/null | sort -nr

echo
echo "=== KNOWN RESEARCH LOCAL COPIES ==="
ROOT="$HOME/bc250-research"
find "$ROOT" -maxdepth 3 -type f \( -name 'vmlinuz-*' -o -name 'initramfs-*.img' \)   -printf '%s\t%p\n' 2>/dev/null | sort -nr | head -100

echo
echo "=== R277 END ==="
} 2>&1 | tee "$OUT"

echo
echo "WROTE=$OUT"
sha256sum "$OUT"
