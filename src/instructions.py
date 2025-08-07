from abc import ABC, abstractmethod
from utils import bytes32_to_int, int_to_bytes32
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from state import MachineState
    from utils import Code




# === Abstract Instruction ===
class Instruction(ABC):
    @abstractmethod
    def execute(self, state: "MachineState"):
        pass

    @staticmethod
    @abstractmethod
    def load(code: "Code") -> "Instruction":
        pass




# === ADD Instruction ===
class ADD(Instruction):
    def __init__(self, r_dst, r_y, r_z, position):
        self.r_dst = r_dst
        self.r_y = r_y
        self.r_z = r_z
        self.position = position

    def execute(self, state: "MachineState"):
        r_y = bytes32_to_int(state.registers[self.r_y])
        r_z = bytes32_to_int(state.registers[self.r_z])

        r_dst = r_y + r_z

        state.registers[self.r_dst] = int_to_bytes32(r_dst)

    @staticmethod
    def load(code: "Code") -> "ADD":
        pos = code.offset - 1
        r_dst = code.read_byte()
        r_y = code.read_byte()
        r_z = code.read_byte()
        return ADD(r_dst, r_y, r_z, pos)

# --- SUB ---
class SUB(Instruction):
    def __init__(self, r_dst, r_y, r_z, position):
        self.r_dst = r_dst
        self.r_y = r_y
        self.r_z = r_z
        self.position = position

    def execute(self, state: "MachineState"):
        r_y = bytes32_to_int(state.registers[self.r_y])
        r_z = bytes32_to_int(state.registers[self.r_z])

        r_dst = r_y - r_z

        state.registers[self.r_dst] = int_to_bytes32(r_dst)

    @staticmethod
    def load(code: "Code") -> "SUB":
        pos = code.offset - 1
        r_dst = code.read_byte()
        r_y = code.read_byte()
        r_z = code.read_byte()
        return SUB(r_dst, r_y, r_z, pos)


# --- MUL ---
class MUL(Instruction):
    def __init__(self, r_dst, r_y, r_z, position):
        self.r_dst = r_dst
        self.r_y = r_y
        self.r_z = r_z
        self.position = position

    def execute(self, state: "MachineState"):
        r_y = bytes32_to_int(state.registers[self.r_y])
        r_z = bytes32_to_int(state.registers[self.r_z])

        r_dst = r_y * r_z

        state.registers[self.r_dst] = int_to_bytes32(r_dst)

    @staticmethod
    def load(code: "Code") -> "MUL":
        pos = code.offset - 1
        r_dst = code.read_byte()
        r_y = code.read_byte()
        r_z = code.read_byte()
        return MUL(r_dst, r_y, r_z, pos)


# --- DIV ---
class DIV(Instruction):
    def __init__(self, r_dst, r_y, r_z, position):
        self.r_dst = r_dst
        self.r_y = r_y
        self.r_z = r_z
        self.position = position

    def execute(self, state: "MachineState"):
        divisor = bytes32_to_int(state.registers[self.r_z])
        if divisor == 0:
            raise ZeroDivisionError(f"Division by zero!")
        r_y = bytes32_to_int(state.registers[self.r_y])

        r_dst = r_y // divisor

        state.registers[self.r_dst] = int_to_bytes32(r_dst)

    @staticmethod
    def load(code: "Code") -> "DIV":
        pos = code.offset - 1
        r_dst = code.read_byte()
        r_y = code.read_byte()
        r_z = code.read_byte()
        return DIV(r_dst, r_y, r_z, pos)


# --- MOD ---
class MOD(Instruction):
    def __init__(self, r_dst, r_y, r_z, position):
        self.r_dst = r_dst
        self.r_y = r_y
        self.r_z = r_z
        self.position = position

    def execute(self, state: "MachineState"):
        divisor = bytes32_to_int(state.registers[self.r_z])
        if divisor == 0:
            raise ZeroDivisionError(f"Modulo by zero!")
        r_y = bytes32_to_int(state.registers[self.r_y])

        r_dst = r_y % divisor

        state.registers[self.r_dst] = int_to_bytes32(r_dst)

    @staticmethod
    def load(code: "Code") -> "MOD":
        pos = code.offset - 1
        r_dst = code.read_byte()
        r_y = code.read_byte()
        r_z = code.read_byte()
        return MOD(r_dst, r_y, r_z, pos)


# --- NEG ---
class NEG(Instruction):
    def __init__(self, r_dst, r_y, position):
        self.r_dst = r_dst
        self.r_y = r_y
        self.position = position

    def execute(self, state: "MachineState"):
        r_y = bytes32_to_int(state.registers[self.r_y])

        r_dst = -r_y

        state.registers[self.r_dst] = int_to_bytes32(r_dst)

    @staticmethod
    def load(code: "Code") -> "NEG":
        pos = code.offset - 1
        r_dst = code.read_byte()
        r_y = code.read_byte()
        return NEG(r_dst, r_y, pos)


# --- INC ---
class INC(Instruction):
    def __init__(self, r_x, position):
        self.r_x = r_x
        self.position = position

    def execute(self, state: "MachineState"):
        r_x = bytes32_to_int(state.registers[self.r_x])
        r_x += 1
        state.registers[self.r_x] = int_to_bytes32(r_x)

    @staticmethod
    def load(code: "Code") -> "INC":
        pos = code.offset - 1
        r_x = code.read_byte()
        return INC(r_x, pos)


# --- DEC ---
class DEC(Instruction):
    def __init__(self, r_x, position):
        self.r_x = r_x
        self.position = position

    def execute(self, state: "MachineState"):
        r_x = bytes32_to_int(state.registers[self.r_x])
        r_x -= 1
        state.registers[self.r_x] = int_to_bytes32(r_x)

    @staticmethod
    def load(code: "Code") -> "DEC":
        pos = code.offset - 1
        r_x = code.read_byte()
        return DEC(r_x, pos)





class AND(Instruction):
    def __init__(self, r_dst, r_y, r_z, position):
        self.r_dst = r_dst
        self.r_y = r_y
        self.r_z = r_z
        self.position = position

    def execute(self, state: "MachineState"):
        y = bytes32_to_int(state.registers[self.r_y])
        z = bytes32_to_int(state.registers[self.r_z])
        result = y & z
        state.registers[self.r_dst] = int_to_bytes32(result)

    @staticmethod
    def load(code: "Code") -> "AND":
        pos = code.offset - 1
        r_dst = code.read_byte()
        r_y = code.read_byte()
        r_z = code.read_byte()
        return AND(r_dst, r_y, r_z, pos)


class OR(Instruction):
    def __init__(self, r_dst, r_y, r_z, position):
        self.r_dst = r_dst
        self.r_y = r_y
        self.r_z = r_z
        self.position = position

    def execute(self, state: "MachineState"):
        y = bytes32_to_int(state.registers[self.r_y])
        z = bytes32_to_int(state.registers[self.r_z])
        result = y | z
        state.registers[self.r_dst] = int_to_bytes32(result)

    @staticmethod
    def load(code: "Code") -> "OR":
        pos = code.offset - 1
        r_dst = code.read_byte()
        r_y = code.read_byte()
        r_z = code.read_byte()
        return OR(r_dst, r_y, r_z, pos)


class XOR(Instruction):
    def __init__(self, r_dst, r_y, r_z, position):
        self.r_dst = r_dst
        self.r_y = r_y
        self.r_z = r_z
        self.position = position

    def execute(self, state: "MachineState"):
        y = bytes32_to_int(state.registers[self.r_y])
        z = bytes32_to_int(state.registers[self.r_z])
        result = y ^ z
        state.registers[self.r_dst] = int_to_bytes32(result)

    @staticmethod
    def load(code: "Code") -> "XOR":
        pos = code.offset - 1
        r_dst = code.read_byte()
        r_y = code.read_byte()
        r_z = code.read_byte()
        return XOR(r_dst, r_y, r_z, pos)


class NOT(Instruction):
    def __init__(self, r_dst, r_y, position):
        self.r_dst = r_dst
        self.r_y = r_y
        self.position = position

    def execute(self, state: "MachineState"):
        y = bytes32_to_int(state.registers[self.r_y])
        result = ~y
        state.registers[self.r_dst] = int_to_bytes32(result)

    @staticmethod
    def load(code: "Code") -> "NOT":
        pos = code.offset - 1
        r_dst = code.read_byte()
        r_y = code.read_byte()
        return NOT(r_dst, r_y, pos)


class SHL(Instruction):
    def __init__(self, r_dst, r_y, r_z, position):
        self.r_dst = r_dst
        self.r_y = r_y
        self.r_z = r_z
        self.position = position

    def execute(self, state: "MachineState"):
        y = bytes32_to_int(state.registers[self.r_y])
        shift = bytes32_to_int(state.registers[self.r_z])
        result = y << shift
        state.registers[self.r_dst] = int_to_bytes32(result)

    @staticmethod
    def load(code: "Code") -> "SHL":
        pos = code.offset - 1
        r_dst = code.read_byte()
        r_y = code.read_byte()
        r_z = code.read_byte()
        return SHL(r_dst, r_y, r_z, pos)


class SHR(Instruction):
    def __init__(self, r_dst, r_y, r_z, position):
        self.r_dst = r_dst
        self.r_y = r_y
        self.r_z = r_z
        self.position = position

    def execute(self, state: "MachineState"):
        y = bytes32_to_int(state.registers[self.r_y])
        shift = bytes32_to_int(state.registers[self.r_z])
        result = y >> shift
        state.registers[self.r_dst] = int_to_bytes32(result)

    @staticmethod
    def load(code: "Code") -> "SHR":
        pos = code.offset - 1
        r_dst = code.read_byte()
        r_y = code.read_byte()
        r_z = code.read_byte()
        return SHR(r_dst, r_y, r_z, pos)





class EQ(Instruction):
    def __init__(self, r_dst, r_y, r_z, position):
        self.r_dst = r_dst
        self.r_y = r_y
        self.r_z = r_z
        self.position = position

    def execute(self, state: "MachineState"):
        val_y = bytes32_to_int(state.registers[self.r_y])
        val_z = bytes32_to_int(state.registers[self.r_z])
        result = 1 if val_y == val_z else 0
        state.registers[self.r_dst] = int_to_bytes32(result)

    @staticmethod
    def load(code: "Code") -> "EQ":
        pos = code.offset - 1
        r_dst = code.read_byte()
        r_y = code.read_byte()
        r_z = code.read_byte()
        return EQ(r_dst, r_y, r_z, pos)

class NEQ(Instruction):
    def __init__(self, r_dst, r_y, r_z, position):
        self.r_dst = r_dst
        self.r_y = r_y
        self.r_z = r_z
        self.position = position

    def execute(self, state: "MachineState"):
        val_y = bytes32_to_int(state.registers[self.r_y])
        val_z = bytes32_to_int(state.registers[self.r_z])
        result = 1 if val_y != val_z else 0
        state.registers[self.r_dst] = int_to_bytes32(result)

    @staticmethod
    def load(code: "Code") -> "NEQ":
        pos = code.offset - 1
        r_dst = code.read_byte()
        r_y = code.read_byte()
        r_z = code.read_byte()
        return NEQ(r_dst, r_y, r_z, pos)

class LT(Instruction):
    def __init__(self, r_dst, r_y, r_z, position):
        self.r_dst = r_dst
        self.r_y = r_y
        self.r_z = r_z
        self.position = position

    def execute(self, state: "MachineState"):
        val_y = bytes32_to_int(state.registers[self.r_y])
        val_z = bytes32_to_int(state.registers[self.r_z])
        result = 1 if val_y < val_z else 0
        state.registers[self.r_dst] = int_to_bytes32(result)

    @staticmethod
    def load(code: "Code") -> "LT":
        pos = code.offset - 1
        r_dst = code.read_byte()
        r_y = code.read_byte()
        r_z = code.read_byte()
        return LT(r_dst, r_y, r_z, pos)

class GT(Instruction):
    def __init__(self, r_dst, r_y, r_z, position):
        self.r_dst = r_dst
        self.r_y = r_y
        self.r_z = r_z
        self.position = position

    def execute(self, state: "MachineState"):
        val_y = bytes32_to_int(state.registers[self.r_y])
        val_z = bytes32_to_int(state.registers[self.r_z])
        result = 1 if val_y > val_z else 0
        state.registers[self.r_dst] = int_to_bytes32(result)

    @staticmethod
    def load(code: "Code") -> "GT":
        pos = code.offset - 1
        r_dst = code.read_byte()
        r_y = code.read_byte()
        r_z = code.read_byte()
        return GT(r_dst, r_y, r_z, pos)

class LTE(Instruction):
    def __init__(self, r_dst, r_y, r_z, position):
        self.r_dst = r_dst
        self.r_y = r_y
        self.r_z = r_z
        self.position = position

    def execute(self, state: "MachineState"):
        val_y = bytes32_to_int(state.registers[self.r_y])
        val_z = bytes32_to_int(state.registers[self.r_z])
        result = 1 if val_y <= val_z else 0
        state.registers[self.r_dst] = int_to_bytes32(result)

    @staticmethod
    def load(code: "Code") -> "LTE":
        pos = code.offset - 1
        r_dst = code.read_byte()
        r_y = code.read_byte()
        r_z = code.read_byte()
        return LTE(r_dst, r_y, r_z, pos)

class GTE(Instruction):
    def __init__(self, r_dst, r_y, r_z, position):
        self.r_dst = r_dst
        self.r_y = r_y
        self.r_z = r_z
        self.position = position

    def execute(self, state: "MachineState"):
        val_y = bytes32_to_int(state.registers[self.r_y])
        val_z = bytes32_to_int(state.registers[self.r_z])
        result = 1 if val_y >= val_z else 0
        state.registers[self.r_dst] = int_to_bytes32(result)

    @staticmethod
    def load(code: "Code") -> "GTE":
        pos = code.offset - 1
        r_dst = code.read_byte()
        r_y = code.read_byte()
        r_z = code.read_byte()
        return GTE(r_dst, r_y, r_z, pos)




class MOV(Instruction):
    def __init__(self, r_dst, r_src, position):
        self.r_dst = r_dst
        self.r_src = r_src
        self.position = position

    def execute(self, state: "MachineState"):
        state.registers[self.r_dst] = state.registers[self.r_src]

    @staticmethod
    def load(code: "Code") -> "MOV":
        pos = code.offset - 1
        r_dst = code.read_byte()
        r_src = code.read_byte()
        return MOV(r_dst, r_src, pos)


class SET1(Instruction):
    def __init__(self, r_dst, value_bytes, position):
        self.r_dst = r_dst
        self.value_bytes = value_bytes.rjust(32, b'\x00')
        self.position = position

    def execute(self, state: "MachineState"):
        state.registers[self.r_dst] = self.value_bytes

    @staticmethod
    def load(code: "Code") -> "SET1":
        pos = code.offset - 1
        r_dst = code.read_byte()
        value_bytes = code.read_bytes(1)
        return SET1(r_dst, value_bytes, pos)


class SET4(Instruction):
    def __init__(self, r_dst, value_bytes, position):
        self.r_dst = r_dst
        self.value_bytes = value_bytes.rjust(32, b'\x00')
        self.position = position

    def execute(self, state: "MachineState"):
        state.registers[self.r_dst] = self.value_bytes

    @staticmethod
    def load(code: "Code") -> "SET4":
        pos = code.offset - 1
        r_dst = code.read_byte()
        value_bytes = code.read_bytes(4)
        return SET4(r_dst, value_bytes, pos)


class SET8(Instruction):
    def __init__(self, r_dst, value_bytes, position):
        self.r_dst = r_dst
        self.value_bytes = value_bytes.rjust(32, b'\x00')
        self.position = position

    def execute(self, state: "MachineState"):
        state.registers[self.r_dst] = self.value_bytes

    @staticmethod
    def load(code: "Code") -> "SET8":
        pos = code.offset - 1
        r_dst = code.read_byte()
        value_bytes = code.read_bytes(8)
        return SET8(r_dst, value_bytes, pos)


class SET20(Instruction):
    def __init__(self, r_dst, value_bytes, position):
        self.r_dst = r_dst
        self.value_bytes = value_bytes.rjust(32, b'\x00')
        self.position = position

    def execute(self, state: "MachineState"):
        state.registers[self.r_dst] = self.value_bytes

    @staticmethod
    def load(code: "Code") -> "SET20":
        pos = code.offset - 1
        r_dst = code.read_byte()
        value_bytes = code.read_bytes(20)
        return SET20(r_dst, value_bytes, pos)


class SET32(Instruction):
    def __init__(self, r_dst, value_bytes, position):
        self.r_dst = r_dst
        # tutaj dopasowujemy do 32 bajtów ale wartość powinna mieć dokładnie 32 bajty
        if len(value_bytes) != 32:
            raise ValueError("SET32 expects exactly 32 bytes")
        self.value_bytes = value_bytes
        self.position = position

    def execute(self, state: "MachineState"):
        state.registers[self.r_dst] = self.value_bytes

    @staticmethod
    def load(code: "Code") -> "SET32":
        pos = code.offset - 1
        r_dst = code.read_byte()
        value_bytes = code.read_bytes(32)
        return SET32(r_dst, value_bytes, pos)


class LOAD(Instruction):
    def __init__(self, r_dst, slot, position):
        self.r_dst = r_dst
        self.slot = slot
        self.position = position

    def execute(self, state: "MachineState"):
        key = self.slot
        val = state.memory.get(key, b'\x00' * 32)
        state.registers[self.r_dst] = val

    @staticmethod
    def load(code: "Code") -> "LOAD":
        pos = code.offset - 1
        r_dst = code.read_byte()
        slot = code.read_bytes(2)
        return LOAD(r_dst, slot, pos)


class STORE(Instruction):
    def __init__(self, slot, r_src, position):
        self.slot = slot
        self.r_src = r_src
        self.position = position

    def execute(self, state: "MachineState"):
        key = self.slot
        state.memory[key] = state.registers[self.r_src]

    @staticmethod
    def load(code: "Code") -> "STORE":
        pos = code.offset - 1
        slot = code.read_bytes(2)
        r_src = code.read_byte()
        return STORE(slot, r_src, pos)


class MLOAD(Instruction):
    def __init__(self, r_dst, slot, position):
        self.r_dst = r_dst
        self.slot = slot
        self.position = position

    def execute(self, state: "MachineState"):
        key = state.registers[self.slot]
        val = state.storage.get(key, b'\x00' * 32)
        state.registers[self.r_dst] = val

    @staticmethod
    def load(code: "Code") -> "MLOAD":
        pos = code.offset - 1
        r_dst = code.read_byte()
        slot = code.read_byte()
        return MLOAD(r_dst, slot, pos)


class MSTORE(Instruction):
    def __init__(self, slot, r_src, position):
        self.slot = slot
        self.r_src = r_src
        self.position = position

    def execute(self, state: "MachineState"):
        key = state.registers[self.slot]
        state.storage[key] = state.registers[self.r_src]

    @staticmethod
    def load(code: "Code") -> "MSTORE":
        pos = code.offset - 1
        slot = code.read_byte()
        r_src = code.read_byte()
        return MSTORE(slot, r_src, pos)



class JMP(Instruction):
    def __init__(self, target_pos, position):
        self.target_pos = int.from_bytes(target_pos, 'big')
        self.position = position

    def execute(self, state: "MachineState"):
        return state.vm.position_map.get(self.target_pos, -1)

    @staticmethod
    def load(code: "Code") -> "JMP":
        pos = code.offset - 1
        target = code.read_bytes(4)
        return JMP(target, pos)


class JMPC(Instruction):
    def __init__(self, r_cond, target_pos, position):
        self.r_cond = r_cond
        self.target_pos = int.from_bytes(target_pos, 'big')
        self.position = position

    def execute(self, state: "MachineState"):
        cond = bytes32_to_int(state.registers[self.r_cond])
        if cond != 0:
            return state.vm.position_map.get(self.target_pos, -1)
        return None

    @staticmethod
    def load(code: "Code") -> "JMPC":
        pos = code.offset - 1
        r_cond = code.read_byte()
        target = code.read_bytes(4)
        return JMPC(r_cond, target, pos)


class END(Instruction):
    def __init__(self, position):
        self.position = position

    def execute(self, state: "MachineState"):
        return 'END'

    @staticmethod
    def load(code: "Code") -> "END":
        return END(code.offset - 1)




class CALLVALUE(Instruction):
    def __init__(self, r_dst, position):
        self.r_dst = r_dst
        self.position = position

    def execute(self, state: "MachineState"):
        state.registers[self.r_dst] = int_to_bytes32(state.get_call_value())

    @staticmethod
    def load(code: "Code") -> "CALLVALUE":
        pos = code.offset - 1
        r_dst = code.read_byte()
        return CALLVALUE(r_dst, pos)

class BALANCE(Instruction):
    def __init__(self, r_dst, position):
        self.r_dst = r_dst
        self.position = position

    def execute(self, state: "MachineState"):
        state.registers[self.r_dst] = int_to_bytes32(state.get_balance())

    @staticmethod
    def load(code: "Code") -> "BALANCE":
        pos = code.offset - 1
        r_dst = code.read_byte()
        return BALANCE(r_dst, pos)

class TRANSFER(Instruction):
    def __init__(self, r_addres, r_amount, position):
        self.r_addres = r_addres
        self.r_amount = r_amount
        self.position = position

    def execute(self, state: "MachineState"):
        address = state.registers[self.r_addres][-20:]
        amount = bytes32_to_int(state.registers[self.r_amount])
        state.add_transfer(address, amount)

    @staticmethod
    def load(code: "Code") -> "TRANSFER":
        pos = code.offset - 1
        r_addres = code.read_byte()
        r_amount = code.read_byte()
        return TRANSFER(r_addres, r_amount, pos)

class SENDER(Instruction):
    def __init__(self, r_dst, position):
        self.r_dst = r_dst
        self.position = position

    def execute(self, state: "MachineState"):
        state.registers[self.r_dst] = state.get_sender().rjust(32, b'\x00')

    @staticmethod
    def load(code: "Code") -> "SENDER":
        pos = code.offset - 1
        r_dst = code.read_byte()
        return SENDER(r_dst, pos)