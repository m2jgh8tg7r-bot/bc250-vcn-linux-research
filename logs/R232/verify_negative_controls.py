"""Check that the CPU tests reject the specific mistaken interpretations.

Only in-memory text-model inputs are changed. No firmware file is edited,
generated, installed, or executed. This is test-sensitivity evidence.
"""
from pathlib import Path
import copy
import json
import verify_models


def rejects(name, address, replacement, check):
    original = verify_models.INS
    changed = copy.deepcopy(original)
    changed[address]["asm"] = replacement
    verify_models.INS = changed
    try:
        try:
            check()
        except AssertionError:
            return {"control": name, "rejected": True, "method": "expectation assertion"}
        except ValueError as exc:
            if address == 0x2121DA and str(exc).startswith("unseeded memory read:"):
                return {"control": name, "rejected": True,
                        "method": "expected row field was never written"}
            raise
        raise RuntimeError("Negative control was not rejected: " + name)
    finally:
        verify_models.INS = original


def main():
    if not __debug__:
        raise RuntimeError("Run without -O")
    results = [
        rejects("Omit pre-boundary factor7, producing alleged stride12", 0x2121DA,
                "mov r0,r0", verify_models.check_row_write),
        rejects("Exclude eligible slot31", 0x201882,
                "cmp r2,#0x1f", verify_models.check_allocator),
        rejects("Treat service selectors as 32 instead of16", 0x2037FC,
                "cmp r2,#0x20", verify_models.check_registration),
    ]
    result = {"result": "PASS", "negative_controls": results, "hardware_access": False,
              "firmware_modified": False, "classification": "PROVEN_STATICALLY"}
    (Path(__file__).parent / "negative-control-results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
