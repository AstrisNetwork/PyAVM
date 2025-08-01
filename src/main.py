from vm import VM

bytecode = "31000120320264413200000018020000010702400000000331010031320042"

vm = VM(bytes.fromhex(bytecode))

vm.state.registers[1] = (5).to_bytes(32, "big", signed=True)
vm.state.registers[2] = (3).to_bytes(32, "big", signed=True)

vm.run()
vm.dump_registers()