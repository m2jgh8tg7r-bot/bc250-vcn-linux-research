#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$HOME/bc250-research/r152-psp-boundary-src}"
OUT="${2:-$HOME/bc250-r274-r152-exact-source-preflight.log}"

AMDGPU="$ROOT/drivers/gpu/drm/amd/amdgpu"
FILES=(
  "$AMDGPU/amdgpu_discovery.c"
  "$AMDGPU/amdgpu_vcn.c"
  "$AMDGPU/vcn_v2_0.c"
  "$AMDGPU/amdgpu_device.c"
)

for f in "${FILES[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "STOP: missing $f" >&2
    exit 2
  fi
done

python3 - "$ROOT" >"$OUT" <<'PY'
from pathlib import Path
import hashlib
import re
import sys

root = Path(sys.argv[1])
amd = root / "drivers/gpu/drm/amd/amdgpu"

targets = {
    "amdgpu_vcn.c": [
        "amdgpu_vcn_sw_init",
        "amdgpu_vcn_setup_ucode",
        "amdgpu_vcn_resume",
    ],
    "vcn_v2_0.c": [
        "vcn_v2_0_sw_init",
        "vcn_v2_0_hw_init",
        "vcn_v2_0_mc_resume",
    ],
}

def sha256(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def extract_function(text, name):
    # Locate a function-name token followed by '(' and then the first body '{'.
    m = re.search(r"\b" + re.escape(name) + r"\s*\(", text)
    if not m:
        return None
    start = text.rfind("\n", 0, m.start()) + 1
    brace = text.find("{", m.end())
    if brace < 0:
        return None
    depth = 0
    i = brace
    while i < len(text):
        c = text[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                end = text.find("\n", i)
                if end < 0:
                    end = len(text)
                return text[start:end]
        i += 1
    return None

print("=== R274 R152 EXACT SOURCE PREFLIGHT ===")
print(f"ROOT={root}")

mk = root / "Makefile"
if mk.exists():
    vals = {}
    for line in mk.read_text(errors="replace").splitlines():
        m = re.match(r"^(VERSION|PATCHLEVEL|SUBLEVEL|EXTRAVERSION)\s*=\s*(.*)$", line)
        if m:
            vals[m.group(1)] = m.group(2).strip()
    print("KERNEL_VERSION=" + ".".join(vals.get(x,"") for x in ("VERSION","PATCHLEVEL","SUBLEVEL")) + vals.get("EXTRAVERSION",""))

print()
print("=== SHA256 ===")
for name in ("amdgpu_discovery.c","amdgpu_vcn.c","vcn_v2_0.c","amdgpu_device.c"):
    p = amd / name
    print(f"{sha256(p)}  {p}")

print()
print("=== DISCOVERY 2.0.3 CONTEXT ===")
p = amd / "amdgpu_discovery.c"
lines = p.read_text(errors="replace").splitlines()
hits = [i for i,l in enumerate(lines) if "IP_VERSION(2, 0, 3)" in l or "IP_VERSION(2,0,3)" in l]
if not hits:
    print("NO_IP_VERSION_2_0_3_HIT")
else:
    for i in hits:
        lo=max(0,i-12); hi=min(len(lines),i+18)
        print(f"--- {p}:{lo+1}-{hi} ---")
        for n in range(lo,hi):
            print(f"{n+1:6d}: {lines[n]}")

for filename,names in targets.items():
    p = amd / filename
    text = p.read_text(errors="replace")
    for name in names:
        print()
        print(f"=== FUNCTION {filename}:{name} ===")
        body = extract_function(text, name)
        if body is None:
            print("NOT_FOUND")
        else:
            print(body)

print()
print("=== HARDWARE QUARANTINE MARKERS / CALLS ===")
patterns = [
    r"vcn_hw_init",
    r"jpeg_hw_init",
    r"hw_phase2",
    r"BC250 R1",
    r"vcn_v2_0_hw_init",
    r"hw_init\(adev\)",
]
for filename in ("amdgpu_device.c","vcn_v2_0.c","amdgpu_vcn.c"):
    p = amd / filename
    lines = p.read_text(errors="replace").splitlines()
    print(f"--- {p} ---")
    shown=set()
    for pat in patterns:
        rx=re.compile(pat)
        for i,l in enumerate(lines):
            if rx.search(l):
                lo=max(0,i-5); hi=min(len(lines),i+7)
                key=(lo,hi)
                if key in shown:
                    continue
                shown.add(key)
                print(f"[{lo+1}-{hi}]")
                for n in range(lo,hi):
                    print(f"{n+1:6d}: {lines[n]}")
                print()

print("=== PREFLIGHT END ===")
PY

echo "WROTE=$OUT"
sha256sum "$OUT"
