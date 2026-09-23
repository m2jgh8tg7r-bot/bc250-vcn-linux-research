"""Wrapper/caller observations without inventing missing SVC67 helper code."""
import json
from pathlib import Path
from text_arm_model import Model, load_index

INS, LITERALS = load_index()


def check_svc64_wrapper():
    count = 0
    for current_class in (0, 1, 2, 4, 5, 6):
        for validation in (0, 0x25, 0x32):
            for allocation in (0, 0xB, 0x30):
                for requested_class in (2, 4, 5, 6):
                    calls = []
                    context, table, holder, output = 0x11000000, 0x12000000, 0x13000000, 0x280060
                    def validate(m):
                        assert (m.get("r0"), m.get("r1")) == (7, output)
                        calls.append("validate")
                        m.put("r0", validation)
                    def allocate(m):
                        assert (m.get("r0"), m.get("r1")) == (requested_class, output)
                        calls.append("allocate")
                        m.put("r0", allocation)
                    m = Model(INS, LITERALS, call_hooks={0x20158C: validate, 0x20180C: allocate})
                    m.memory.seed(context + 0x4B, 7, 1)
                    m.memory.seed(context + 4, output)
                    m.memory.seed(table + 7 * 0x5C, current_class, 1)
                    m.memory.seed(holder, table)
                    m.memory.seed(holder + 4, context)
                    m.put("r0", context)
                    m.put("r5", requested_class)
                    m.put("r7", 7)
                    m.put("r8", holder + 4)
                    m.put("lr", holder)
                    m.run(0x2049BA, stop_before=(0x204F12,))
                    expected = 0xE if current_class != 1 else validation or allocation
                    assert m.get("r4") == expected
                    assert calls == ([] if current_class != 1 else ["validate"] if validation else ["validate", "allocate"])
                    count += 1
    return count


def check_selector_class():
    count = 0
    for returned_value in list(range(17)) + [0x2F, 0xFFFF0008, 0xFFFFFFFF]:
        def property_helper(m):
            m.put("r0", returned_value)
        m = Model(INS, LITERALS, call_hooks={0x20FE64: property_helper})
        m.put("r4", 0x20A100)
        m.run(0x211BC6, stop_before=(0x211BE2,))
        assert m.get("r5") == returned_value
        assert m.get("r10") == (4 if returned_value in (2, 3, 4) else 6)
        count += 1
    return count


def check_svc74_wrapper():
    count = 0
    for service in (0, 1, 3, 15, 16):
        for argument in (0, 1, 31, 32, 255, 256, 257, 0xFFFFFFFF):
            for occupied in (False, True):
                slot = argument & 255
                m = Model(INS, LITERALS)
                m.memory.seed(0x11000004, argument)
                m.memory.zero(0x69B0, 256)
                m.memory.zero(0x8430, 16)
                if slot < 32:
                    m.memory.seed(0x69B0 + 8 * slot, 0x80000001 if occupied else 1)
                m.put("r0", 0x11000000)
                m.put("r5", service)
                m.run(0x204C82, stop_before=(0x204F12,))
                expected = 0x25 if slot >= 32 or not occupied else 0x2E if service >= 16 else 0
                assert m.get("r4") == expected
                if expected == 0:
                    assert m.memory.read(0x8430 + service, 1) == slot
                count += 1
    return count


def check_svc67_caller():
    count = 0
    for slot in (1, 7, 31):
        for size in (0x1000, 0x19000, 0xD0000):
            for returned_pointer in (0, 0x100000, 0x900000):
                for status in (0, 0xB, 0x25):
                    output = 0x10000068
                    row = 0x286000 + slot * 0x54
                    def svc(m, number):
                        assert number == 0x67
                        assert (m.get("r0"), m.get("r1"), m.get("r2")) == (slot, size, output)
                        m.memory.seed(output, returned_pointer)
                        m.put("r0", status)
                    m = Model(INS, LITERALS, svc_hook=svc)
                    m.memory.seed(0x206080, 0x280000)
                    m.memory.seed(m.get("sp") + 0x60, slot, 1)
                    m.memory.seed(m.get("sp"), size)
                    m.memory.seed(output, 0xA5A5A5A5)
                    m.memory.seed(row, 0xA5A5A5A5)
                    m.memory.seed(row + 4, 0xA5A5A5A5)
                    m.put("r7", 0x206080)
                    m.run(0x211D56, stop_before=(0x211D9C, 0x212224))
                    if status == 0:
                        assert m.memory.read(row) == returned_pointer
                        assert m.memory.read(row + 4) == size
                    else:
                        assert m.memory.read(row) == 0xA5A5A5A5
                        assert m.memory.read(row + 4) == 0xA5A5A5A5
                    count += 1
    return count


def main():
    result = {"classification": "PROVEN_STATICALLY", "hardware_access": False,
              "svc64_wrapper_cases": check_svc64_wrapper(),
              "svc74_wrapper_cases": check_svc74_wrapper(),
              "selector_class_cases": check_selector_class(),
              "svc67_caller_cases": check_svc67_caller(),
              "result": "PASS", "limits": ["Validation, allocation, property, and SVC67 results are hypothetical hooks",
                 "SVC67 worker implementation is not recovered or modeled"]}
    (Path(__file__).parent / "wrapper-model-results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
