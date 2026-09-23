"""Offline differential checks of saved allocator/registration/walker text.

The instruction-level model is compared with small independently expressed
contracts. SVC results are assumptions supplied by hooks, never observations.
"""
from pathlib import Path
import json
import random
from text_arm_model import Model, load_index, MASK

INS, LITERALS = load_index()
COUNTS = {}


def fresh(**kw):
    return Model(INS, LITERALS, **kw)


def check_allocator():
    rng = random.Random(232)
    cases = []
    # Each possible earliest free index, plus complete exhaustion; vary lower
    # bits to test signed occupancy, preserved metadata, and first-fit priority.
    for item_class in (2, 4, 5, 6):
        for free in range(1, 33):
            for special_state in (0, 1, 0xFE, 0xFF):
                for trial in range(8):
                    words = [rng.randrange(1 << 31) | (1 << 31) for _ in range(32)]
                    for i in range(free, 32):
                        if i == free or rng.getrandbits(1):
                            words[i] &= ~(1 << 31)
                    initial_highwater = rng.randrange(32)
                    m = fresh()
                    table, output = 0x69B0, 0x11000000
                    for i, word in enumerate(words):
                        m.memory.seed(table + i * 8, word)
                        m.memory.seed(table + i * 8 + 4, 0xA0A0A0A0)
                    m.memory.seed(0x6006, special_state, 1)
                    m.memory.seed(0x60B4, initial_highwater, 1)
                    m.memory.seed(output, 0xFF, 1)
                    m.put("r0", item_class)
                    m.put("r1", output)
                    m.run(0x20180C)
                    expected_error = (0xB if free == 32 else
                                      0x30 if item_class == 2 and special_state != 0xFF else 0)
                    assert m.get("r0") == expected_error
                    if expected_error:
                        assert m.memory.read(output, 1) == 0xFF
                        assert all(m.memory.read(table + i * 8) == words[i] for i in range(32))
                        assert m.memory.read(0x60B4, 1) == initial_highwater
                    else:
                        expected_flags = {2: 0x511, 4: 0x4541, 5: 0x5401, 6: 0x4441}[item_class]
                        assert m.memory.read(output, 1) == free
                        assert m.memory.read(table + free * 8) == words[free] | item_class | (1 << 31)
                        assert m.memory.read(table + free * 8 + 4) == expected_flags
                        assert m.memory.read(0x60B4, 1) == max(initial_highwater, free)
                        assert all(m.memory.read(table + i * 8) == words[i]
                                   for i in range(32) if i != free)
                    cases.append((item_class, free, special_state, trial))
    # The class-1 initialization branch is outside the ordinary loader classes:
    # success does not write the output pointer. Do not generalize 1..31 to it.
    m = fresh()
    m.memory.zero(0x69B0, 256)
    m.memory.seed(0x11000000, 0xFF, 1)
    m.put("r0", 1)
    m.put("r1", 0x11000000)
    m.run(0x20180C)
    assert m.get("r0") == 0
    assert m.memory.read(0x69B0) == 0x80000001
    assert m.memory.read(0x69B4) == 0x4505
    assert m.memory.read(0x11000000, 1) == 0xFF
    COUNTS["allocator_differential_cases"] = len(cases)
    COUNTS["allocator_class1_edge_cases"] = 1


def check_registration():
    count = 0
    # The 0x37ec helper validates destination before service selector. This is
    # different from the user row's slot calculation and from F2 dispatch.
    for service in list(range(17)) + [0xFF, 0xFFFFFFFF]:
        for destination in list(range(33)) + [0xFF, 0xFFFFFFFF]:
            for occupied in (False, True):
                m = fresh()
                m.memory.zero(0x8430, 16)
                m.memory.zero(0x69B0, 256)
                if destination < 32:
                    m.memory.seed(0x69B0 + destination * 8, 0x80000004 if occupied else 4)
                m.put("r0", service)
                m.put("r1", destination)
                m.run(0x2037EC)
                valid_destination = destination < 32 and occupied
                expected = 0x25 if not valid_destination else 0x2E if service >= 16 else 0
                assert m.get("r0") == expected, (service, destination, occupied, m.get("r0"))
                for i in range(16):
                    assert m.memory.read(0x8430 + i, 1) == (destination if expected == 0 and i == service else 0)
                count += 1
    COUNTS["registration_differential_cases"] = count


def check_row_write():
    count = 0
    for slot in range(32):
        for service in (0, 1, 2, 3, 4, 13, 15, 16, 0xFFFFFFFF):
            expected_row = 0x280000 + 0x6000 + slot * 0x54
            def svc(m, number):
                assert number == 0x74
                assert m.get("r0") == service
                assert m.get("r1") == slot
                assert m.memory.read(expected_row + 0x18) == service
                m.halted = True
            m = fresh(svc_hook=svc)
            m.memory.seed(0x206080, 0x280000)
            m.memory.seed(m.get("sp") + 0x60, slot, 1)
            m.put("r5", service)
            m.run(0x2121D6)
            assert [x for x in m.memory.writes if x[0] < 0x10000000] == [(expected_row + 0x18, service, 4)]
            count += 1
    COUNTS["row_write_differential_cases"] = count


def check_loader_post_registration():
    count = 0
    # Execute from the actual SVC74 call through the caller-visible output byte.
    # Stop on entry to cleanup, rather than simulate unknown cleanup services.
    for service in (0, 1, 2, 3, 4, 13, 15):
        for registration_result in (0, 0x25, 0x2E):
            for f2_result in (0, 0x2F, 0xFFFF0008):
                events = []
                output = 0x11000000
                def svc(m, number):
                    if number == 0x74:
                        assert m.get("r0") == service and m.get("r1") == 7
                        m.put("r0", registration_result)
                    elif number == 0xF2:
                        assert m.get("r0") == service
                        command = m.memory.read(m.get("r1"))
                        assert command == 0xFFFF0002
                        events.append(command)
                        m.put("r0", f2_result)
                    elif number == 0x63:
                        m.halted = True
                    else:
                        raise ValueError(number)
                m = fresh(svc_hook=svc)
                m.memory.seed(m.get("sp") + 0x60, 7, 1)
                m.memory.seed(m.get("sp") + 0x148, output)
                m.memory.seed(output, 0xFF, 1)
                m.memory.seed(0x20607D, 0, 1)
                m.put("r5", service)
                m.put("r0", service)
                m.put("r1", 7)
                m.run(0x2121F6)
                invoked = registration_result == 0 and service not in (1, 3)
                assert bool(events) == invoked
                success = registration_result == 0 and (not invoked or f2_result == 0)
                assert m.memory.read(output, 1) == (7 if success else 0xFF)
                assert m.memory.read(0x20607D, 1) == int(success and service == 2)
                expected_return = registration_result if registration_result else f2_result if invoked else 0
                assert m.get("r7") == expected_return
                count += 1
    COUNTS["loader_registration_lifecycle_cases"] = count


def run_walker(mode, rows, response=None, budget=10000):
    events, callbacks = [], []
    def svc(m, number):
        if number == 0xF2:
            service, arg = m.get("r0"), m.get("r1")
            command = None if arg == 1 else m.memory.read(arg)
            event = {"service": service, "argument_is_immediate": arg == 1,
                     "command": command, "pc": hex(m.pc)}
            events.append(event)
            m.put("r0", response(event, len(events)) if response else 0)
        elif number in (0x96, 0x5E, 0x7A, 0x61, 0x5F, 0x60):
            m.put("r0", 0)
        else:
            raise ValueError(number)
    def zero(m):
        m.memory.zero(m.get("r0"), m.get("r1"))
        m.put("r0", 0)
    def callback(m):
        callbacks.append(hex(m.pc))
        m.put("r0", 0)
    hooks = {0x20E28C: zero}
    hooks.update({a: callback for a in (0x211814, 0x212800, 0x211774, 0x212804)})
    m = fresh(svc_hook=svc, call_hooks=hooks)
    m.memory.zero(0x2060F0, 8)
    m.memory.seed(0x2060F5, mode, 1)
    m.memory.seed(0x206080, 0x280000)
    m.memory.seed(0x2060D8, 7)
    m.memory.seed(0x2060E0, 0x12000000)
    m.memory.seed(0x2060E4, 0x13000000)
    m.memory.zero(0x286000, 32 * 0x54)
    for slot, tag, service in rows:
        m.memory.seed(0x286000 + slot * 0x54 + 8, tag)
        m.memory.seed(0x286000 + slot * 0x54 + 0x18, service)
    m.run(0x20FC50, budget)
    return m, events, callbacks


def check_walker():
    count = 0
    # Mode values are modeled as data; the caller rejects zero before entry.
    # Additional mode 3 documents the encoded fallback without claiming it
    # is a real observed mode.
    for mode in (1, 2, 3):
        for special_slot in (0, 7, 31):
            for other_slot in (1, 16, 30):
                rows = [(special_slot, 0x5244, 3), (other_slot, 0x5244, 4),
                        (2, 0x4154, 8)]
                m, events, callbacks = run_walker(mode, rows)
                first_command = 0xFFFF0000 if mode == 1 else 0xFFFF0004
                second_command = 0xFFFF0001 if mode == 1 else 0xFFFF0005
                expected = []
                for slot, tag, service in sorted(rows, reverse=True):
                    if tag != 0x5244:
                        continue
                    if service == 3:
                        if mode == 2:
                            expected.append((3, True, None))
                    else:
                        expected.append((service, False, first_command))
                for slot, tag, service in sorted(rows):
                    if tag == 0x5244 and service != 3:
                        expected.append((service, False, second_command))
                assert [(e["service"], e["argument_is_immediate"], e["command"]) for e in events] == expected
                assert m.memory.read(0x12000718) == 0x80000000
                assert m.memory.read(0x2060F5, 1) == 0
                assert len(callbacks) == 4
                count += 1
    # Descending phase retries the SAME service on any nonzero r0. This does
    # not prove retry is safe or terminates on a real PSP.
    m, events, _ = run_walker(1, [(7, 0x5244, 4)],
                             lambda event, n: 0x2F if n == 1 else 0)
    assert [(e["service"], e["command"]) for e in events] == [
        (4, 0xFFFF0000), (4, 0xFFFF0000), (4, 0xFFFF0001)]
    assert m.memory.read(0x12000718) == 0x80000000
    # Ascending failure returns to cleanup and never visits the later service.
    m, events, callbacks = run_walker(1, [(7, 0x5244, 4), (9, 0x5244, 2)],
        lambda event, n: 0x2F if event["command"] == 0xFFFF0001 else 0)
    assert [(e["service"], e["command"]) for e in events] == [
        (2, 0xFFFF0000), (4, 0xFFFF0000), (4, 0xFFFF0001)]
    assert m.memory.read(0x12000718) == 0x40000000 and not callbacks
    assert m.memory.read(0x2060F5, 1) == 0
    # Service-3's immediate call has no r4 result assignment in this walker.
    m, events, callbacks = run_walker(2, [(7, 0x5244, 3)], lambda event, n: 0x2F)
    assert len(events) == 1 and events[0]["argument_is_immediate"]
    assert m.memory.read(0x12000718) == 0x80000000 and len(callbacks) == 4
    # An unchanging failure in descending phase is a loop, not a completed
    # failed operation; the fail-closed step budget must detect it.
    try:
        run_walker(1, [(7, 0x5244, 4)], lambda event, n: 0x2F, budget=500)
    except ValueError as exc:
        assert "budget exhausted" in str(exc)
    else:
        raise AssertionError("expected non-terminating retry under stubbed failure")
    COUNTS["walker_order_and_mode_cases"] = count
    COUNTS["walker_failure_behavior_cases"] = 4


def check_property_request():
    count = 0
    for cached_layout in (0, 1, 2, 3):
        for probe_return in (0, 0x2F):
            for probed_layout in (0, 1, 2):
                for property_return in (0, 5, 0xFFFF0008):
                    for property_value in (1, 3, 4, 13, 0xFFFFFFFF):
                        requests = []
                        image_pointer = 0x20A100
                        output_pointer = 0x287324
                        def svc(m, number):
                            assert number == 0xF2 and m.get("r0") == 1
                            p = m.get("r1")
                            command = m.memory.read(p)
                            assert m.memory.read(p + 4) == 2
                            requests.append(command)
                            if command == 0x103B:
                                m.memory.seed(p + 0x38, probed_layout)
                                m.put("r0", probe_return)
                            elif command == 0x1009:
                                layout = cached_layout or (1 if probe_return else probed_layout)
                                if layout == 1:
                                    assert m.memory.read(p + 0x38) == image_pointer
                                    name = m.memory.read(p + 0x3C)
                                    assert m.memory.read(p + 0x40) == 16
                                    output = m.memory.read(p + 0x44)
                                else:
                                    assert m.memory.read(p + 8) == image_pointer
                                    assert m.memory.read(p + 0xC) == 0x1000
                                    name = m.memory.read(p + 0x10)
                                    assert m.memory.read(p + 0x14) == 16
                                    output = m.memory.read(p + 0x18)
                                    assert m.memory.read(p + 0x1C) == 0x84
                                assert name == 0x20FE8C  # artificial saved-text coordinate
                                assert output == output_pointer
                                if property_return == 0:
                                    m.memory.seed(output + 4, property_value)
                                m.put("r0", property_return)
                            else:
                                raise ValueError(hex(command))
                        def zero(m):
                            m.memory.zero(m.get("r0"), m.get("r1"))
                            m.put("r0", 0)
                        def string_length(m):
                            assert m.get("r0") == 0x20FE8C
                            m.put("r0", 15)
                        m = fresh(svc_hook=svc, call_hooks={0x20E28C: zero, 0x20E09C: string_length})
                        m.memory.seed(0x206080, 0x280000)
                        m.memory.seed(0x206140, cached_layout)
                        m.memory.seed(output_pointer + 4, 0xA5A5A5A5)
                        m.put("r0", image_pointer)
                        m.run(0x20FE64)
                        expected = property_value if property_return == 0 else property_return
                        assert m.get("r0") == expected
                        assert requests == ([0x103B, 0x1009] if cached_layout == 0 else [0x1009])
                        count += 1
    COUNTS["driver_property_request_cases"] = count


def main():
    check_allocator()
    check_registration()
    check_row_write()
    check_loader_post_registration()
    check_walker()
    check_property_request()
    result = {"classification": "PROVEN_STATICALLY", "model": "saved instruction-text subset",
              "counts": COUNTS, "result": "PASS", "hardware_access": False,
              "limits": ["SVC/call hooks are assumptions", "No live TOS identity or occupancy proof",
                         "No firmware acceptance or VCN execution proof"]}
    (Path(__file__).parent / "model-results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
