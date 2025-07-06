from typing import List, Dict
from abc import ABC, abstractmethod

class VM:
    def __init__(self):
        self.registers: list = [0] * (2**16)        # 64 rejestry: r0-r63
        self.storage: Dict[bytes, int] = {}  # Storage, klucze 32 bajty
        self.pc = 0                      # Program counter
        self.running = True
        self.call_stack: List[int] = []  # Stos adresów powrotu
        self.bytecode: bytes = b""
        self.func_map: Dict[int, int] = {}  # Mapowanie funkcji id -> adres w bytecode

        # Mapa opcode -> klasa instrukcji
        self.instruction_map: Dict[int, Instruction] = {
            0x00: ADD(0x00),
            0x01: SUB(0x01),
            0x02: MUL(0x02),
            0x03: DIV(0x03),
            0x04: MOD(0x04),
            0x05: INC(0x05),
            0x06: DEC(0x06),

            0x10: EQUAL(0x10),
            0x11: BIGGER(0x11),
            0x12: LOWER(0x12),

            0x20: SET4(0x20),
            0x21: SET8(0x21),
            0x22: SET16(0x22),
            0x23: SET20(0x23),
            0x24: SET(0x24),

            0x25: MOV(0x25),
            0x26: STORE(0x26),
            0x27: LOAD(0x27),

            0x30: FNS(0x30),
            0x31: FNE(0x31),
            0x32: GOTO(0x32),
            0x33: IFS(0x33),
            0x34: IFE(0x34),
            0x35: END(0x35),
        }

    def load_program(self, code: bytes):
        self.bytecode = code
        self.pc = 0
        self.running = True
        self.call_stack.clear()
        self.func_map.clear()
        self._build_function_map()
    
    def _build_function_map(self):
        pc = 0
        while pc < len(self.bytecode):
            opcode = self.bytecode[pc]
            instr = self.instruction_map.get(opcode)

            if instr is None:
                raise ValueError(f"Nieznany opcode: {opcode:#x} w bajcie {pc}")

            if opcode == 0x30:  # FNS
                func_id = (self.bytecode[pc+1] << 8) | self.bytecode[pc+2]
                self.func_map[func_id] = pc + instr.get_full_length()

            pc += instr.get_full_length()


    # def _build_function_map(self):
    #     # Przeszukaj bytecode w poszukiwaniu FNS <func_id>
    #     pc = 0
    #     while pc < len(self.bytecode):
    #         opcode = self.bytecode[pc]
    #         if opcode == 0x30:  # FNS
    #             func_id = (self.bytecode[pc+1] << 8) | self.bytecode[pc+2]
    #             self.func_map[func_id] = pc + 3  # adres pierwszej instrukcji po FNS
    #             pc += 3
    #         else:
    #             pc += 1
    #             # Skok po argumentach w zależności od opcode - uproszczenie:
    #             # Tutaj opcjonalnie możesz dodać lepsze przeskakiwanie
    #             # ale w tej wersji przyjmujemy 1 bajt arg lub ręcznie rozszerzamy.
    #             # Dla poprawności interpreter będzie działał, gdy funkcje nie są w głębokim zagnieżdżeniu.

    def read_byte(self) -> int:
        val = self.bytecode[self.pc]
        self.pc += 1
        return val

    def read_bytes(self, n: int) -> bytes:
        val = self.bytecode[self.pc:self.pc+n]
        self.pc += n
        return val

    def read_reg(self) -> int:
        return int.from_bytes(self.read_bytes(2), "big")

    def read_u16(self) -> int:
        b1 = self.read_byte()
        b2 = self.read_byte()
        return (b1 << 8) | b2

    def run(self):
        while self.running and self.pc < len(self.bytecode):
            opcode = self.read_byte()
            instr = self.instruction_map.get(opcode)
            print(instr)
            if instr is None:
                raise RuntimeError(f'Nieznany opcode 0x{opcode:02X} na pc={self.pc-1}')
            instr.execute(self)


class Instruction:
    def __init__(self, opcode: int):
        self.opcode = opcode

    def execute(self, vm):
        raise NotImplementedError()

    def get_full_length(self) -> int:
        return 1  # domyślnie tylko opcode


# --- Definicje instrukcji ---

class ADD(Instruction):
    def execute(self, vm: VM):
        r3 = vm.read_reg()
        r1 = vm.read_reg()
        r2 = vm.read_reg()
        vm.registers[r3] = vm.registers[r1] + vm.registers[r2]
    
    def get_full_length(self) -> int:
        return 7

class SUB(Instruction):
    def execute(self, vm: VM):
        r3 = vm.read_reg()
        r1 = vm.read_reg()
        r2 = vm.read_reg()
        vm.registers[r3] = vm.registers[r1] - vm.registers[r2]
    
    def get_full_length(self) -> int:
        return 7

class MUL(Instruction):
    def execute(self, vm: VM):
        r3 = vm.read_reg()
        r1 = vm.read_reg()
        r2 = vm.read_reg()
        vm.registers[r3] = vm.registers[r1] * vm.registers[r2]
    
    def get_full_length(self) -> int:
        return 7

class DIV(Instruction):
    def execute(self, vm: VM):
        r3 = vm.read_reg()
        r1 = vm.read_reg()
        r2 = vm.read_reg()
        divisor = vm.registers[r2]
        if divisor == 0:
            raise ZeroDivisionError("Division by zero")
        vm.registers[r3] = vm.registers[r1] // divisor
    
    def get_full_length(self) -> int:
        return 7

class MOD(Instruction):
    def execute(self, vm: VM):
        r3 = vm.read_reg()
        r1 = vm.read_reg()
        r2 = vm.read_reg()
        divisor = vm.registers[r2]
        if divisor == 0:
            raise ZeroDivisionError("Modulo by zero")
        vm.registers[r3] = vm.registers[r1] % divisor
    
    def get_full_length(self) -> int:
        return 7

class INC(Instruction):
    def execute(self, vm: VM):
        r1 = vm.read_reg()
        vm.registers[r1] += 1
    
    def get_full_length(self) -> int:
        return 3

class DEC(Instruction):
    def execute(self, vm: VM):
        r1 = vm.read_reg()
        vm.registers[r1] -= 1
    
    def get_full_length(self) -> int:
        return 3

class EQUAL(Instruction):
    def execute(self, vm: VM):
        r3 = vm.read_reg()
        r1 = vm.read_reg()
        r2 = vm.read_reg()
        vm.registers[r3] = 1 if vm.registers[r1] == vm.registers[r2] else 0
    
    def get_full_length(self) -> int:
        return 5

class BIGGER(Instruction):
    def execute(self, vm: VM):
        r3 = vm.read_reg()
        r1 = vm.read_reg()
        r2 = vm.read_reg()
        vm.registers[r3] = 1 if vm.registers[r1] > vm.registers[r2] else 0
    
    def get_full_length(self) -> int:
        return 5

class LOWER(Instruction):
    def execute(self, vm: VM):
        r3 = vm.read_reg()
        r1 = vm.read_reg()
        r2 = vm.read_reg()
        vm.registers[r3] = 1 if vm.registers[r1] < vm.registers[r2] else 0
    
    def get_full_length(self) -> int:
        return 5

class SET4(Instruction):
    def execute(self, vm: VM):
        r1 = vm.read_reg()
        val_bytes = vm.read_bytes(4)
        vm.registers[r1] = int.from_bytes(val_bytes, 'big')
    
    def get_full_length(self) -> int:
        return 7

class SET8(Instruction):
    def execute(self, vm: VM):
        r1 = vm.read_reg()
        val_bytes = vm.read_bytes(8)
        vm.registers[r1] = int.from_bytes(val_bytes, 'big')
    
    def get_full_length(self) -> int:
        return 11

class SET16(Instruction):
    def execute(self, vm: VM):
        r1 = vm.read_reg()
        val_bytes = vm.read_bytes(16)
        vm.registers[r1] = int.from_bytes(val_bytes, 'big')
    
    def get_full_length(self) -> int:
        return 19

class SET20(Instruction):
    def execute(self, vm: VM):
        r1 = vm.read_reg()
        val_bytes = vm.read_bytes(20)
        vm.registers[r1] = int.from_bytes(val_bytes, 'big')
    
    def get_full_length(self) -> int:
        return 23

class SET(Instruction):
    def execute(self, vm: VM):
        r1 = vm.read_reg()
        val_bytes = vm.read_bytes(32)
        vm.registers[r1] = int.from_bytes(val_bytes, 'big')
    
    def get_full_length(self) -> int:
        return 35

class MOV(Instruction):
    def execute(self, vm: VM):
        r1 = vm.read_reg()
        r2 = vm.read_reg()
        vm.registers[r1] = vm.registers[r2]
    
    def get_full_length(self) -> int:
        return 5

class STORE(Instruction):
    def execute(self, vm: VM):
        key = vm.read_bytes(32)
        r1 = vm.read_reg()
        vm.storage[key] = vm.registers[r1]
    
    def get_full_length(self) -> int:
        return 35

class LOAD(Instruction):
    def execute(self, vm: VM):
        r1 = vm.read_reg()
        key = vm.read_bytes(32)
        vm.registers[r1] = vm.storage.get(key, 0)
    
    def get_full_length(self) -> int:
        return 35

class FNS(Instruction):
    def execute(self, vm: VM):
        # Definicja funkcji: przeskocz całą zawartość od FNS do odpowiadającego FNE
        # najpierw pomiń dwu-bajtowy func_id
        vm.pc += 2
        depth = 1
        # dopóki nie zamkniesz tej etykiety
        while vm.pc < len(vm.bytecode) and depth > 0:
            opcode = vm.bytecode[vm.pc]
            instr = vm.instruction_map.get(opcode)
            # jeśli to ponowne FNS, to wchodzisz głębiej
            if opcode == 0x30:
                depth += 1
            # jeśli to FNE, to schodzisz w głąb
            elif opcode == 0x31:
                depth -= 1
            # skocz o pełną długość tej instrukcji
            vm.pc += instr.get_full_length() if instr else 1
    
    def get_full_length(self) -> int:
        return 3

class FNE(Instruction):
    def execute(self, vm: VM):
        if not vm.call_stack:
            raise RuntimeError("Stack underflow przy FNE")
        # pobieramy adres powrotu i ustawiamy PC
        vm.pc = vm.call_stack.pop()

    def get_full_length(self) -> int:
        return 1

class GOTO(Instruction):
    def execute(self, vm: VM):
        func_id = vm.read_u16()
        if func_id not in vm.func_map:
            raise RuntimeError(f"Nieznana funkcja ID {func_id}")
        # Zapamiętaj adres powrotu i skocz
        vm.call_stack.append(vm.pc)
        vm.pc = vm.func_map[func_id]
    
    def get_full_length(self) -> int:
        return 3

class IFS(Instruction):
    def execute(self, vm: VM):
        r1 = vm.read_reg()
        if vm.registers[r1]:
            # Szukamy odpowiadającego IFE (0x34), uwzględniając zagnieżdżenia IFS
            depth = 1
            while vm.pc < len(vm.bytecode) and depth > 0:
                opcode = vm.bytecode[vm.pc]
                if opcode == 0x33:  # IFS
                    depth += 1
                elif opcode == 0x34:  # IFE
                    depth -= 1
                vm.pc += 1
            if depth != 0:
                raise RuntimeError("Brak odpowiadającego IFE")
    
    def get_full_length(self) -> int:
        return 6

class IFE(Instruction):
    def execute(self, vm: VM):
        # Znacznik końca bloku if - nic do wykonania
        pass

class END(Instruction):
    def execute(self, vm: VM):
        vm.running = False


# --- Przykład i test ---

if __name__ == "__main__":
    vm = VM()

    # Przykładowy program:
    # FNS 0x0001:
    # SET4 r1, 10
    # SET4 r2, 20
    # ADD r16, r1, r2  (wynik w rejestrach zwracanych)
    # FNE
    # GOTO 0x0001
    # END

    program = bytes.fromhex("3000012000010000000a20000200000032000010000100023132000135")

    vm.load_program(bytes(program))
    vm.run()

    print("r16 =", vm.registers[16])  # Powinno być 30
