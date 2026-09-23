"""Saved-text lifetime and F2 pre-dispatch checks; no hardware operations."""
from pathlib import Path
import json
from text_arm_model import Model, load_index

INS, LITERALS = load_index()


def cleanup(slot, service, base=0x290000, tag=0x5244, svc_result=0, detach_result=0):
    events = []
    row = 0x286000 + slot * 0x54
    def svc(m, number):
        event = [hex(number), m.get("r0"), m.get("r1")]
        if number == 0xF2:
            event.append(m.memory.read(m.get("r1")))
        events.append(event)
        if number not in (0x5E, 0x5F, 0xF2, 0x74, 0x85, 0x65):
            raise ValueError(event)
        m.put("r0", svc_result)
    def free(m):
        assert (m.get("r0"), m.get("r1")) == (base, 0x5000)
        events.append(["free", m.get("r0"), m.get("r1")])
        m.put("r0", 0)
    def detach(m):
        assert m.get("r0") == slot
        events.append(["detach", slot])
        m.put("r0", detach_result)
    def finish(m):
        assert (m.get("r0"), m.get("r1")) == (slot, 0)
        events.append(["finish", slot])
        m.put("r0", 0)
    m = Model(INS, LITERALS, svc_hook=svc,
              call_hooks={0x20EBDC: free, 0x20F168: detach, 0x20FADC: finish})
    m.memory.seed(0x2060C4, 9)
    m.memory.seed(0x206080, 0x280000)
    m.memory.seed(0x20607D, 1, 1)
    m.memory.zero(row, 0x54)
    m.memory.seed(row, base)
    m.memory.seed(row + 4, 0x5000)
    m.memory.seed(row + 8, tag)
    m.memory.seed(row + 0x18, service)
    m.memory.seed(row + 0x1D, 0xAA, 1)
    m.put("r0", slot)
    m.run(0x213020)
    return m, events, row


def check_cleanup():
    count = 0
    for slot in (0, 1, 7, 31, 32, 0xFFFFFFFF):
        for service in (1, 2, 3, 4, 15, 16):
            for base in (0, 0x290000):
                for svc_result in (0, 0x2F, 0xFFFF0008):
                    for detach_result in (0, 0x29):
                        m, events, row = cleanup(slot, service, base,
                                                svc_result=svc_result,
                                                detach_result=detach_result)
                        codes = [x[0] for x in events]
                        active = slot < 32 and service != 1 and base != 0
                        expected_return = (0x25 if slot >= 32 else 0 if service == 1 else
                                           0x36 if base == 0 else detach_result)
                        assert m.get("r0") == expected_return
                        if active:
                            assert codes == ["0x5e", "0xf2", "0x74", "0x85", "free",
                                             "detach", "0x65", "finish", "0x5f"]
                            assert events[1][1:] == [service, events[1][2], 0xFFFF0003]
                            assert events[2][1:] == [service, 0]
                            assert m.memory.read(row) == 0 and m.memory.read(row + 8) == 0
                            assert m.memory.read(row + 0x1D, 1) == 0
                            # +0x18 is stale after logical removal, not cleared.
                            assert m.memory.read(row + 0x18) == service
                            assert m.memory.read(0x20607D, 1) == (0 if service == 2 else 1)
                        else:
                            assert codes == ([] if slot >= 32 else ["0x5e", "0x5f"])
                            assert m.memory.read(row) == base
                            assert m.memory.read(row + 8) == 0x5244
                        count += 1
    return count


def f2_gate(service, destination, caller_class=1, caller_flags=0x80000080,
            stack=0x280044, busy=0, nested=0xFF):
    m = Model(INS, LITERALS)
    context, contexts, caller = 0x11000000, 0x12000000, 7
    m.memory.seed(0x6010, context)
    m.memory.seed(0x6054, contexts)
    m.memory.zero(0x8430, 16)
    if service < 16:
        m.memory.seed(0x8430 + service, destination, 1)
    m.memory.zero(context, 0x80)
    m.memory.seed(context + 0x4B, caller, 1)
    m.memory.seed(context + 0x4C, nested, 1)
    m.memory.seed(context + 0x34, stack)
    m.memory.seed(0x69B0 + 8 * caller, caller_flags)
    m.memory.seed(contexts + caller * 0x5C, caller_class, 1)
    m.memory.seed(contexts + destination * 0x5C + 0x34, busy, 1)
    m.put("r0", service)
    m.put("r1", 0x281000)
    # Successful address validation reaches the first context copy. Stop there:
    # no scheduler or service execution is modeled.
    def boundary(model):
        model.halted = True
    m.call_hooks[0x200470] = boundary
    m.run(0x201AB8)
    return m


def check_f2_gates():
    count = 0
    for service in (0, 1, 2, 3, 15, 16, 0xFFFFFFFF):
        for destination in (0, 1, 3, 31):
            for caller_class in (1, 4, 5):
                for permission in (False, True):
                    for stack in (0, 0x280044, 0x10000045):
                        for busy in (0, 1, 7, 15, 0xFF):
                            flags = 0x80000000 | (0x80 if permission else 0)
                            # Class 4 takes a different nested-dispatch branch;
                            # keep this experiment at earlier gate outcomes.
                            if service < 16 and destination and service != 3 and caller_class == 4 and permission and stack == 0x280044 and busy not in (15, 0xFF):
                                continue
                            if service == 1 and destination and caller_class == 4 and stack == 0x280044 and busy not in (15, 0xFF):
                                continue
                            m = f2_gate(service, destination, caller_class, flags, stack, busy)
                            expected = (0x2E if service >= 16 else 0x2F if destination == 0 else
                                        0xE if service != 1 and (not permission or service == 3 and caller_class != 1) else
                                        0x32 if ((stack - 0x44) & 0xFFFFFFFF) > 0x10000000 else
                                        0x31 if busy & 15 == 15 else
                                        0x32 if caller_class == 5 else None)
                            if expected is None:
                                assert m.halted and m.pc == 0x201BAA
                                first_free = next(i for i in range(4) if not busy & (1 << i))
                                assert m.get("r4") == first_free
                            else:
                                assert not m.halted and m.get("r0") == expected
                            count += 1
    return count


def main():
    result = {"classification": "PROVEN_STATICALLY", "hardware_access": False,
              "cleanup_cases": check_cleanup(), "f2_predispatch_cases": check_f2_gates(),
              "result": "PASS", "limits": ["Cleanup service return values are hypothetical hooks",
                  "F2 success stops before context copy, scheduling, or service execution"]}
    (Path(__file__).parent / "lifetime-model-results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
