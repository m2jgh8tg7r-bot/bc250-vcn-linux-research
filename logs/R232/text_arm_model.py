"""Small fail-closed interpreter for already-saved ARM/Thumb instruction text.

This is a research model, not a PSP emulator. It does not decode firmware,
execute guest machine code, access devices, or implement PSP services. Hooks
explicitly stand in for unknown calls/SVCs. Unsupported instructions fail.
Only the subset needed for bounded saved control-flow experiments is supported.
"""
from pathlib import Path
import json
import re

MASK = 0xFFFFFFFF
STOP = 0xFFFFF000


def signed(x):
    return x - (1 << 32) if x & (1 << 31) else x


def split_args(s):
    result, start, depth = [], 0, 0
    for i, c in enumerate(s):
        if c in "[{":
            depth += 1
        elif c in "]}":
            depth -= 1
        elif c == "," and depth == 0:
            result.append(s[start:i].strip())
            start = i + 1
    result.append(s[start:].strip())
    return result


class Memory:
    def __init__(self):
        self.data = {}
        self.writes = []

    def seed(self, addr, value, size=4):
        for i in range(size):
            self.data[(addr + i) & MASK] = (value >> (i * 8)) & 255

    def read(self, addr, size=4):
        missing = [hex((addr + i) & MASK) for i in range(size)
                   if ((addr + i) & MASK) not in self.data]
        if missing:
            raise ValueError("unseeded memory read: " + ", ".join(missing))
        return sum(self.data[(addr + i) & MASK] << (8 * i) for i in range(size))

    def write(self, addr, value, size=4):
        self.writes.append((addr & MASK, value & ((1 << (size * 8)) - 1), size))
        self.seed(addr, value, size)

    def zero(self, addr, size):
        for i in range(size):
            self.seed(addr + i, 0, 1)


class Model:
    executed = set()
    def __init__(self, instructions, literals, svc_hook=None, call_hooks=None):
        self.instructions = instructions
        self.regs = {"r" + str(i): 0 for i in range(16)}
        self.regs.update(r13=0x10000000, r14=STOP)
        self.memory = Memory()
        for addr, value in literals.items():
            self.memory.seed(addr, value)
        self.n = self.z = self.c = self.v = False
        self.pc = None
        self.trace = []
        self.svc_calls = []
        self.svc_hook = svc_hook
        self.call_hooks = call_hooks or {}
        self.halted = False

    @staticmethod
    def reg(name):
        return {"sp": "r13", "lr": "r14", "pc": "r15"}.get(name, name)

    def get(self, name):
        name = name.strip()
        if name.startswith("#"):
            return int(name[1:], 0) & MASK
        if name.startswith("0x"):
            return int(name, 16) & MASK
        reg = self.reg(name)
        if reg == "r15":
            return (self.pc + 4) & MASK
        return self.regs[reg]

    def put(self, name, value):
        self.regs[self.reg(name)] = value & MASK

    def nz(self, value):
        self.n = bool(value & (1 << 31))
        self.z = (value & MASK) == 0

    def subtract_flags(self, left, right, value):
        self.nz(value)
        self.c = left >= right
        self.v = bool(((left ^ right) & (left ^ value)) & (1 << 31))

    def add_flags(self, left, right, value):
        self.nz(value)
        self.c = left + right > MASK
        self.v = bool((~(left ^ right) & (left ^ value)) & (1 << 31))

    def operand(self, args):
        value = self.get(args[0])
        if len(args) == 1:
            return value
        if len(args) != 2:
            raise ValueError(args)
        kind, amount = args[1].split()
        amount = self.get(amount)
        if kind == "lsl":
            return (value << amount) & MASK
        if kind == "lsr":
            return value >> amount
        if kind == "asr":
            return signed(value) >> amount & MASK
        raise ValueError(args)

    def address(self, expr):
        if not (expr.startswith("[") and expr.endswith("]")):
            raise ValueError("unsupported addressing: " + expr)
        args = split_args(expr[1:-1])
        return (self.get(args[0]) + (self.operand(args[1:]) if len(args) > 1 else 0)) & MASK

    def condition(self, suffix):
        return {
            "eq": self.z, "ne": not self.z,
            "cs": self.c, "hs": self.c, "cc": not self.c, "lo": not self.c,
            "mi": self.n, "pl": not self.n,
            "vs": self.v, "vc": not self.v,
            "hi": self.c and not self.z, "ls": not self.c or self.z,
            "ge": self.n == self.v, "lt": self.n != self.v,
            "gt": not self.z and self.n == self.v,
            "le": self.z or self.n != self.v,
        }[suffix]

    def run(self, start, limit=10000, stop_before=()):
        self.pc = start
        for _ in range(limit):
            if self.pc == STOP or self.halted or self.pc in stop_before:
                return self
            if self.pc not in self.instructions:
                raise ValueError("missing saved instruction " + hex(self.pc))
            entry = self.instructions[self.pc]
            if entry["bytes"] is None:
                raise ValueError("instruction lacks saved bytes: " + hex(self.pc))
            asm = entry["asm"]
            self.executed.add(self.pc)
            self.trace.append((self.pc, asm))
            next_pc = self.pc + len(bytes.fromhex(entry["bytes"]))
            op, _, rest = asm.partition(" ")
            op = op.removesuffix(".w")
            args = split_args(rest) if rest else []
            if op in ("push", "pop"):
                regs = sorted(args[0][1:-1].split(","), key=lambda x: int(self.reg(x)[1:]))
                if op == "push":
                    sp = self.get("sp") - 4 * len(regs)
                    self.put("sp", sp)
                    for i, reg in enumerate(regs):
                        self.memory.write(sp + 4 * i, self.get(reg))
                else:
                    sp = self.get("sp")
                    for i, reg in enumerate(regs):
                        value = self.memory.read(sp + 4 * i)
                        if self.reg(reg) == "r15":
                            next_pc = value & ~1
                        else:
                            self.put(reg, value)
                    self.put("sp", sp + 4 * len(regs))
            elif op in ("mov", "movs", "movw"):
                value = self.get(args[1])
                self.put(args[0], value)
                if op == "movs":
                    self.nz(value)
            elif op == "adr":
                # Ghidra already resolved this PC-relative operand. The model
                # retains artificial code coordinates; it is not a runtime VA.
                self.put(args[0], int(args[1][1:-1], 16))
            elif op in ("add", "adds", "addw", "sub", "subs", "subw", "rsb"):
                if self.reg(args[0]) == "r15":
                    raise ValueError("arithmetic writes to PC are outside this model")
                left = self.get(args[1] if len(args) >= 3 else args[0])
                right = self.operand(args[2:] if len(args) >= 3 else args[1:])
                if op == "rsb":
                    left, right = right, left
                value = (left + right if op.startswith("add") else left - right) & MASK
                self.put(args[0], value)
                if op in ("adds", "subs"):
                    (self.add_flags if op == "adds" else self.subtract_flags)(left, right, value)
            elif op == "cmp":
                left, right = self.get(args[0]), self.get(args[1])
                self.subtract_flags(left, right, (left - right) & MASK)
            elif op == "tst":
                self.nz(self.get(args[0]) & self.get(args[1]))
            elif op in ("orr", "orrs", "and", "ands", "bic"):
                left = self.get(args[1] if len(args) >= 3 else args[0])
                right = self.operand(args[2:] if len(args) >= 3 else args[1:])
                value = (left | right if op.startswith("orr") else
                         left & ~right if op == "bic" else left & right) & MASK
                self.put(args[0], value)
                if op.endswith("s"):
                    self.nz(value)
            elif op == "uxtb":
                self.put(args[0], self.get(args[1]) & 255)
            elif op in ("lsl", "lsls", "lsr", "lsrs", "asr", "asrs"):
                value, amount = self.get(args[1]), self.get(args[2])
                if amount > 32:
                    raise ValueError("shift outside model subset")
                if op.startswith("lsl"):
                    result = value << amount & MASK
                    carry = (value >> (32 - amount)) & 1 if amount else self.c
                elif op.startswith("lsr"):
                    result = value >> amount
                    carry = (value >> (amount - 1)) & 1 if amount else self.c
                else:
                    result = signed(value) >> amount & MASK
                    carry = (value >> (amount - 1)) & 1 if amount else self.c
                self.put(args[0], result)
                if op.endswith("s"):
                    self.nz(result)
                    self.c = bool(carry)
            elif op in ("ldr", "ldrb", "ldrh", "str", "strb", "strh"):
                size = 1 if op.endswith("b") else 2 if op.endswith("h") else 4
                addr = self.address(args[1])
                if op.startswith("ldr"):
                    self.put(args[0], self.memory.read(addr, size))
                else:
                    self.memory.write(addr, self.get(args[0]), size)
            elif op in ("ldrd", "strd"):
                addr = self.address(args[2])
                for i, reg in enumerate(args[:2]):
                    if op == "ldrd":
                        self.put(reg, self.memory.read(addr + i * 4))
                    else:
                        self.memory.write(addr + i * 4, self.get(reg))
            elif op == "stmia":
                require_writeback = args[0].endswith("!")
                if not require_writeback:
                    raise ValueError("STM without writeback outside this model")
                base_reg = args[0][:-1]
                regs = sorted(args[1][1:-1].split(","), key=lambda x: int(self.reg(x)[1:]))
                if base_reg in regs:
                    raise ValueError("STM base in register list outside this model")
                addr = self.get(base_reg)
                for i, reg in enumerate(regs):
                    self.memory.write(addr + i * 4, self.get(reg))
                self.put(base_reg, addr + 4 * len(regs))
            elif op in ("cbz", "cbnz"):
                if (self.get(args[0]) == 0) == (op == "cbz"):
                    next_pc = int(args[1], 16)
            elif op == "b":
                next_pc = int(args[0], 16)
            elif op in ("beq", "bne", "bcs", "bcc", "bmi", "bpl", "bge", "blt", "bgt", "ble", "bhi", "bls"):
                if self.condition(op[1:]):
                    next_pc = int(args[0], 16)
            elif op in ("bl", "blx"):
                target = int(args[0], 16)
                self.put("lr", next_pc)
                if target in self.call_hooks:
                    self.call_hooks[target](self)
                else:
                    next_pc = target
            elif op == "bx":
                next_pc = self.get(args[0]) & ~1
            elif op == "svc":
                number = int(args[0], 16)
                self.svc_calls.append({"pc": hex(self.pc), "svc": hex(number),
                                       "args": [self.get("r" + str(i)) for i in range(4)]})
                if self.svc_hook is None:
                    raise ValueError("SVC encountered without explicit hook")
                self.svc_hook(self, number)
            elif op != "nop":
                raise ValueError("unsupported saved instruction: " + hex(self.pc) + " " + asm)
            self.pc = next_pc
        raise ValueError("instruction budget exhausted; possible intentional retry loop")


def load_index():
    data = json.loads((Path(__file__).parent / "saved-instruction-index.json").read_text())
    return ({int(k, 16): v for k, v in data["instructions"].items()},
            {int(k, 16): int(v, 16) for k, v in data["literals"].items()})
