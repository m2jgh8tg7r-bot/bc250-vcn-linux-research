"""Keep host command 8, service-1 request 0x1024, and external op-id 8 distinct."""
from pathlib import Path
import json
from text_arm_model import Model, load_index

INS, LITERALS = load_index()


def zero(m):
    m.memory.zero(m.get("r0"), m.get("r1"))
    m.put("r0", 0)


def check_requests():
    count = 0
    for layout in (1, 2, 3):
        for selector in (0, 1, 7, 31, 0xFF):
            for status in (0, 0x2F, 0xFFFF0008):
                for entry, command in ((0x20F168, 0x1001), (0x20F18C, 0x1024)):
                    events = []
                    def svc(m, number):
                        assert number == 0xF2 and m.get("r0") == 1
                        p = m.get("r1")
                        assert m.memory.read(p) == command
                        assert m.memory.read(p + 4) == 2
                        if command == 0x1001:
                            assert m.memory.read(p + 0x38) == selector
                        elif layout == 1:
                            assert [m.memory.read(p + x) for x in (0x38, 0x3C, 0x40)] == [0x281000, 0x282360, selector]
                        else:
                            assert [m.memory.read(p + x) for x in (8, 12, 16, 20, 0x40)] == [0x281000, 0x400, 0x282360, 0x400, selector]
                        events.append(command)
                        m.put("r0", status)
                    m = Model(INS, LITERALS, svc_hook=svc, call_hooks={0x20E28C: zero})
                    m.memory.seed(0x206140, layout)
                    m.put("r0", selector if command == 0x1001 else 0x281000)
                    m.put("r1", 0x282360)
                    m.put("r2", selector)
                    m.run(entry)
                    assert m.get("r0") == status and events == [command]
                    count += 1
    return count


def main():
    result = {"classification": "PROVEN_STATICALLY", "hardware_access": False,
              "service_request_cases": check_requests(), "result": "PASS",
              "limits": ["Request construction and return propagation only; service body is not modeled",
                         "No equivalence to external operation-array id 8 or t28 handler is assumed"]}
    (Path(__file__).parent / "service-request-results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
