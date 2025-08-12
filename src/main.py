from assembler import assemble
from vm import VM, VMInt

asm = """

add:
    GETPARAM r0, #0
    GETPARAM r1, #1
    ADD r2, r0, r1
    RETURN #0, r2

"""

bytecode, _ = assemble(asm)

vm = VM(bytecode, {})
vm.state.set_param(0, VMInt(150))
vm.state.set_param(1, VMInt(300))
vm.run()
result = VMInt.load(vm.state.returns[0]).get()
print(result)