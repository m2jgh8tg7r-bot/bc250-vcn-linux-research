#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/bc250-research}"
OUT="${2:-$HOME/bc250-r278-retirement-candidate-audit.log}"

rows=(
"R138|/boot/initramfs-7.2.3-r138.img|$ROOT/r138-boot-repair/initramfs-7.2.3-r138.img"
"R141|/boot/initramfs-7.2.3-r141-diagnostic.img|$ROOT/r141-swinit-diagnostic/initramfs-7.2.3-r141-diagnostic.img"
"R157|/boot/initramfs-7.2.3-r157-psp-control.img|$ROOT/r157-psp-observation-control/initramfs-7.2.3-r157-psp-control.img"
"R173|/boot/initramfs-7.2.3-r173-observation.img|$ROOT/r173-request-observation/initramfs-7.2.3-r173-observation.img"
"R180|/boot/initramfs-7.2.3-r180-observation.img|$ROOT/r180-load-response-observation/initramfs-7.2.3-r180-observation.img"
"R197|/boot/initramfs-7.2.3-r197-firmware.img|$ROOT/r197-firmware-response-comparison/initramfs-7.2.3-r197-firmware.img"
)

{
echo "=== R278 RETIREMENT CANDIDATE AUDIT (READ-ONLY) ==="
date -Ins

echo
echo "=== BOOTLOADER REFERENCE SEARCH ==="
for d in /boot/loader /boot/loader.1 /boot/grub2 /boot/efi /efi; do
  if [[ -e "$d" ]]; then
    echo "--- $d ---"
    sudo grep -R -n -E       'initramfs-7\.2\.3-(r138|r141-diagnostic|r157-psp-control|r173-observation|r180-observation|r197-firmware)\.img'       "$d" 2>/dev/null || true
  fi
done

echo
echo "=== EXACT IMAGE HASH PAIRS ==="
for row in "${rows[@]}"; do
  IFS='|' read -r name boot local <<< "$row"
  echo
  echo "--- $name ---"
  echo "BOOT=$boot"
  echo "LOCAL=$local"

  if [[ -f "$local" ]]; then
    LOCAL_SIZE="$(stat -c '%s' "$local")"
    LOCAL_SHA="$(sha256sum "$local" | awk '{print $1}')"
    echo "LOCAL_PRESENT=YES"
    echo "LOCAL_SIZE=$LOCAL_SIZE"
    echo "LOCAL_SHA256=$LOCAL_SHA"
  else
    echo "LOCAL_PRESENT=NO"
    LOCAL_SHA=""
  fi

  if sudo test -f "$boot"; then
    BOOT_SIZE="$(sudo stat -c '%s' "$boot")"
    BOOT_SHA="$(sudo sha256sum "$boot" | awk '{print $1}')"
    echo "BOOT_PRESENT=YES"
    echo "BOOT_SIZE=$BOOT_SIZE"
    echo "BOOT_SHA256=$BOOT_SHA"
  else
    echo "BOOT_PRESENT=NO"
    BOOT_SHA=""
  fi

  if [[ -n "$LOCAL_SHA" && -n "$BOOT_SHA" && "$LOCAL_SHA" == "$BOOT_SHA" ]]; then
    echo "LOCAL_BOOT_HASH_MATCH=YES"
  else
    echo "LOCAL_BOOT_HASH_MATCH=NO"
  fi
done

echo
echo "=== CURRENT BLS FILES ==="
for d in /boot/loader/entries /boot/loader.1/entries /boot/efi/loader/entries; do
  if sudo test -d "$d"; then
    echo "--- $d ---"
    sudo find "$d" -maxdepth 1 -type f -print | sort
  fi
done

echo
echo "=== CURRENT /BOOT FREE ==="
df -h /boot
df -B1 /boot

echo
echo "R278_READ_ONLY=YES"
echo "NO_FILES_MOVED=YES"
echo "NO_FILES_DELETED=YES"
echo "NO_BOOT_CONFIG_CHANGED=YES"
} 2>&1 | tee "$OUT"

echo
echo "WROTE=$OUT"
sha256sum "$OUT"
