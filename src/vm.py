from state import MachineState
from utils import Code
from instructions_reg import INSTRUCTION_SET
from utils import bytes32_to_int

# === The VM Class ===
class VM:
    def __init__(self, bytecode: bytes, abi: dict):
        self.code = Code(bytecode)
        self.abi = abi
        self.state = MachineState()
        self.state.vm = self
        self.instructions = []

    def load_instructions(self):
        self.position_map = {}

        while self.code.offset < len(self.code.byte_code):
            pos = self.code.offset
            opcode = self.code.read_byte()
            instr_cls = INSTRUCTION_SET.get(opcode)
            if not instr_cls:
                raise ValueError(f"Unknown opcode: {opcode:#02x}")
            instr = instr_cls.load(self.code)
            self.instructions.append(instr)
            self.position_map[pos] = len(self.instructions) - 1

    def execute(self, pc: int = 0):
        self.pc = self.position_map.get(pc)
        while self.pc < len(self.instructions):
            instr = self.instructions[self.pc]
            jump_result = instr.execute(self.state)
            
            if isinstance(jump_result, int):  # jeśli instrukcja wykonała skok
                self.pc = jump_result
            elif jump_result == 'END':
                break
            else:
                self.pc += 1

    def run(self, pc: int = 0):
        self.load_instructions()
        self.execute(pc)

    def dump_registers(self):
        for i, val in enumerate(self.state.registers):
            if val != b'\x00' * 32:
                print(f"r{i} = {bytes32_to_int(val)}")
                # print(f"r{i} = {val}")