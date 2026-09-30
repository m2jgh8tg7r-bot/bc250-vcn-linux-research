#!/usr/bin/env bash
set -euo pipefail

D="${1:-$HOME/bc250-research/r274b-native-layout-build-v2}"
OUT="${2:-$HOME/bc250-r275-artifact-audit-v2.log}"

MOD="$D/amdgpu.ko.unstripped"
PATCH="$D/r274b-native-layout.patch"
BASE="$D/amdgpu_vcn.c.baseline"
CAND="$D/amdgpu_vcn.c.candidate"

EXPECTED_MOD="b1138dd396c0a0e31b3431b9da1a50ae1f564a0ef102864e63e4a75763576ef5"
EXPECTED_PATCH="a46b83447bce8301f2516d561b270a25ddad84b8401652b04e7228c118421921"
EXPECTED_BASE="09d8076366f028a1e6cf416c3989147a35ad488fb1a8e311490e345109d8d099"
EXPECTED_CAND="06e1595fe8f90503664bc242fefa2cc151d7b43f15f762998ad476e3160ddd67"

for f in "$MOD" "$PATCH" "$BASE" "$CAND"; do
  [[ -f "$f" ]] || { echo "STOP: missing $f" >&2; exit 2; }
done

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

GEN="$TMP/generated.patch"
MODKO="$TMP/amdgpu-r274b.ko"

set +e
diff -u   --label a/drivers/gpu/drm/amd/amdgpu/amdgpu_vcn.c   --label b/drivers/gpu/drm/amd/amdgpu/amdgpu_vcn.c   "$BASE" "$CAND" > "$GEN"
DRC=$?
set -e
if [[ "$DRC" -ne 1 ]]; then
  echo "STOP: diff return=$DRC; expected 1 for differing files" >&2
  exit 3
fi

cp -- "$MOD" "$MODKO"

{
  echo "=== R275 ARTIFACT AUDIT V2 ==="
  date -Ins

  echo
  echo "=== EXACT INPUT HASHES ==="
  for spec in     "$MOD:$EXPECTED_MOD"     "$PATCH:$EXPECTED_PATCH"     "$BASE:$EXPECTED_BASE"     "$CAND:$EXPECTED_CAND"
  do
    f="${spec%%:*}"
    exp="${spec##*:}"
    got="$(sha256sum "$f" | awk '{print $1}')"
    echo "$f"
    echo " expected=$exp"
    echo " actual=$got"
    [[ "$got" == "$exp" ]] || { echo "HASH_MATCH=NO"; exit 4; }
    echo " HASH_MATCH=YES"
  done

  echo
  echo "=== PATCH CORRESPONDENCE WITHOUT patch(1) ==="
  GH="$(sha256sum "$GEN" | awk '{print $1}')"
  PH="$(sha256sum "$PATCH" | awk '{print $1}')"
  echo "generated_diff_sha256=$GH"
  echo "retained_patch_sha256=$PH"
  if cmp -s "$GEN" "$PATCH"; then
    echo "GENERATED_DIFF_EQUALS_RETAINED_PATCH=YES"
  else
    echo "GENERATED_DIFF_EQUALS_RETAINED_PATCH=NO"
    diff -u "$PATCH" "$GEN" | head -100 || true
    exit 5
  fi

  echo
  echo "=== MODULE ELF IDENTITY ==="
  file "$MOD" || true
  sha256sum "$MOD"

  echo
  echo "=== MODULE METADATA ==="
  if command -v modinfo >/dev/null 2>&1; then
    if modinfo "$MODKO" >/dev/null 2>&1; then
      modinfo "$MODKO" | grep -E '^(filename|license|description|author|version|srcversion|vermagic|signer|sig_key|sig_hashalgo):' || true
      echo "MODINFO_READABLE=YES"
    else
      echo "MODINFO_READABLE=NO"
    fi
  else
    echo "MODINFO_COMMAND=ABSENT"
  fi

  echo
  echo "=== EMBEDDED MODINFO FALLBACK ==="
  strings "$MOD" | grep -E '^(vermagic|srcversion|license|description|author)=' | head -30 || true

  echo
  echo "=== BUILD ID ==="
  if command -v readelf >/dev/null 2>&1; then
    BID="$(readelf -n "$MOD" 2>/dev/null | sed -n 's/.*Build ID: //p' | head -1)"
    if [[ -n "$BID" ]]; then
      echo "BUILD_ID=$BID"
    else
      echo "BUILD_ID=NOT_PRESENT_OR_NOT_FOUND"
    fi
  else
    echo "READELF_COMMAND=ABSENT"
  fi

  echo
  echo "=== REQUIRED MARKERS ==="
  FAIL=0
  for m in     "BC250 R141 psp_vcn_enrollment: skipped (R79 guard)"     "BC250 R141 vcn_hw_init: skipped"     "BC250 R274B direct_copy:"
  do
    if grep -aFq "$m" "$MOD"; then
      echo "PRESENT: $m"
    else
      echo "MISSING: $m"
      FAIL=1
    fi
  done
  [[ "$FAIL" -eq 0 ]] || exit 6

  echo
  echo "=== OLD R274-A MARKER ==="
  if grep -aFq "BC250 R274 direct_copy:" "$MOD"; then
    echo "R274A_MARKER_PRESENT=YES"
    exit 7
  else
    echo "R274A_MARKER_PRESENT=NO"
  fi

  echo
  echo "=== PATCH ADDED CONTROL TOKENS ==="
  if grep '^+' "$PATCH" | grep -Ev '^\+\+\+' | grep -E 'WREG|RREG|SMN|vcn_v2_0_start|amdgpu_ring_init|LOAD_IP_FW|psp_cmd|doorbell|soft_reset'; then
    echo "ADDED_HARDWARE_CONTROL_TOKENS=FOUND"
    exit 8
  else
    echo "ADDED_HARDWARE_CONTROL_TOKENS=NONE"
  fi

  echo
  echo "R275_ARTIFACT_AUDIT_V2=PASS"
  echo "NO_MODULE_INSTALLED=YES"
  echo "NO_BOOT_ARTIFACT_CHANGED=YES"
} 2>&1 | tee "$OUT"

echo
echo "WROTE=$OUT"
sha256sum "$OUT"
