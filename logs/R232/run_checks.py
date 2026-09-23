"""Run all offline R232 checks and record saved-text instruction coverage."""
from pathlib import Path
import json
import hashlib
import verify_models
import verify_lifetime
import verify_wrappers
import verify_service_requests
from text_arm_model import Model

ROOT = Path(__file__).parent


def main():
    if not __debug__:
        raise RuntimeError("Run without -O: assertions are the research checks")
    verify_models.main()
    verify_lifetime.main()
    verify_wrappers.main()
    verify_service_requests.main()
    results = [json.loads((ROOT / p).read_text()) for p in
               ("model-results.json", "lifetime-model-results.json", "wrapper-model-results.json", "service-request-results.json")]
    count = sum(results[0]["counts"].values())
    count += sum(v for r in results[1:] for k, v in r.items() if k.endswith("_cases"))
    result = {"result": "PASS", "total_cases": count,
              "executed_saved_instruction_count": len(Model.executed),
              "executed_saved_instruction_addresses": [hex(x) for x in sorted(Model.executed)],
              "hardware_access": False, "hardware_mutation": False,
              "limits": "Modeled instructions and explicit hooks only; no complete firmware emulator",
              "code_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
                              for p in ("text_arm_model.py", "verify_models.py", "verify_lifetime.py", "verify_wrappers.py", "verify_service_requests.py")}}
    (ROOT / "suite-results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "executed_saved_instruction_addresses"}, indent=2))


if __name__ == "__main__":
    main()
