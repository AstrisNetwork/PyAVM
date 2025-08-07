INSTRUCTION_TABLE = {}

def register(opcode_name):
    def wrapper(fn):
        INSTRUCTION_TABLE[opcode_name.upper()] = fn
        return fn
    return wrapper

def parse_register(token: str) -> int:
    token = token.strip(",").lower()
    if not token.startswith("r"):
        raise ValueError(f"Invalid register {token}")
    return int(token[1:])



def parse_bytes_token(token: str) -> bytes:
    # Token expected to be hex string like 0x01, 0x1234 etc. or decimal number
    token = token.strip(",")
    if token.startswith("0x"):
        val = int(token, 16)
    else:
        val = int(token, 10)
    # Convert to bytes without leading zeros (minimal length)
    return val.to_bytes((val.bit_length() + 7) // 8 or 1, byteorder="big", signed=True)

def pad_bytes(data: bytes, length: int) -> bytes:
    # Pad on the left (big endian)
    return b'\x00' * (length - len(data)) + data


# === ALU ===
@register("ADD")
def asm_add(tokens):
    return bytes([0x00, parse_register(tokens[1]), parse_register(tokens[2]), parse_register(tokens[3])])

@register("SUB")
def asm_sub(tokens):
    return bytes([0x01, parse_register(tokens[1]), parse_register(tokens[2]), parse_register(tokens[3])])

@register("MUL")
def asm_mul(tokens):
    return bytes([0x02, parse_register(tokens[1]), parse_register(tokens[2]), parse_register(tokens[3])])

@register("DIV")
def asm_div(tokens):
    return bytes([0x03, parse_register(tokens[1]), parse_register(tokens[2]), parse_register(tokens[3])])

@register("MOD")
def asm_mod(tokens):
    return bytes([0x04, parse_register(tokens[1]), parse_register(tokens[2]), parse_register(tokens[3])])

@register("NEG")
def asm_neg(tokens):
    return bytes([0x05, parse_register(tokens[1]), parse_register(tokens[2])])

@register("INC")
def asm_inc(tokens):
    return bytes([0x06, parse_register(tokens[1])])

@register("DEC")
def asm_dec(tokens):
    return bytes([0x07, parse_register(tokens[1])])


# === Bitwise ===
@register("AND")
def asm_and(tokens):
    return bytes([0x10, parse_register(tokens[1]), parse_register(tokens[2]), parse_register(tokens[3])])

@register("OR")
def asm_or(tokens):
    return bytes([0x11, parse_register(tokens[1]), parse_register(tokens[2]), parse_register(tokens[3])])

@register("XOR")
def asm_xor(tokens):
    return bytes([0x12, parse_register(tokens[1]), parse_register(tokens[2]), parse_register(tokens[3])])

@register("NOT")
def asm_not(tokens):
    return bytes([0x13, parse_register(tokens[1]), parse_register(tokens[2])])

@register("SHL")
def asm_shl(tokens):
    return bytes([0x14, parse_register(tokens[1]), parse_register(tokens[2]), parse_register(tokens[3])])

@register("SHR")
def asm_shr(tokens):
    return bytes([0x15, parse_register(tokens[1]), parse_register(tokens[2]), parse_register(tokens[3])])



@register("EQ")
def asm_eq(tokens):
    return bytes([0x20, parse_register(tokens[1]), parse_register(tokens[2]), parse_register(tokens[3])])

@register("NEQ")
def asm_neq(tokens):
    return bytes([0x21, parse_register(tokens[1]), parse_register(tokens[2]), parse_register(tokens[3])])

@register("LT")
def asm_lt(tokens):
    return bytes([0x22, parse_register(tokens[1]), parse_register(tokens[2]), parse_register(tokens[3])])

@register("GT")
def asm_gt(tokens):
    return bytes([0x23, parse_register(tokens[1]), parse_register(tokens[2]), parse_register(tokens[3])])

@register("LTE")
def asm_lte(tokens):
    return bytes([0x24, parse_register(tokens[1]), parse_register(tokens[2]), parse_register(tokens[3])])

@register("GTE")
def asm_gte(tokens):
    return bytes([0x25, parse_register(tokens[1]), parse_register(tokens[2]), parse_register(tokens[3])])



@register("MOV")
def asm_mov(tokens):
    r_dst = parse_register(tokens[1])
    r_src = parse_register(tokens[2])
    return bytes([0x30, r_dst, r_src])

def pad_bytes(b: bytes, length: int) -> bytes:
    return b.rjust(length, b'\x00')

def parse_bytes_token(token: str) -> bytes:
    # Przyjmijmy, że token to hex string np. "0x1234" lub "1234"
    if token.startswith("0x") or token.startswith("0X"):
        token = token[2:]
    elif token.startswith("#"):
        token = hex(int(token[1:]))[2:]
    if len(token) % 2:
        token = "0" + token
    return bytes.fromhex(token)

@register("SET1")
def asm_set1(tokens):
    r_dst = parse_register(tokens[1])
    val_bytes = pad_bytes(parse_bytes_token(tokens[2]), 1)
    return bytes([0x31, r_dst]) + val_bytes[-1:]

@register("SET4")
def asm_set4(tokens):
    r_dst = parse_register(tokens[1])
    val_bytes = pad_bytes(parse_bytes_token(tokens[2]), 4)
    return bytes([0x32, r_dst]) + val_bytes[-4:]

@register("SET8")
def asm_set8(tokens):
    r_dst = parse_register(tokens[1])
    val_bytes = pad_bytes(parse_bytes_token(tokens[2]), 8)
    return bytes([0x33, r_dst]) + val_bytes[-8:]

@register("SET20")
def asm_set20(tokens):
    r_dst = parse_register(tokens[1])
    val_bytes = pad_bytes(parse_bytes_token(tokens[2]), 20)
    return bytes([0x34, r_dst]) + val_bytes[-20:]

@register("SET32")
def asm_set32(tokens):
    r_dst = parse_register(tokens[1])
    val_bytes = pad_bytes(parse_bytes_token(tokens[2]), 32)
    return bytes([0x35, r_dst]) + val_bytes[-32:]

@register("LOAD")
def asm_load(tokens):
    r_dst = parse_register(tokens[1])
    slot = int(tokens[2])
    slot_bytes = slot.to_bytes(2, "big")
    return bytes([0x36, r_dst]) + slot_bytes

@register("STORE")
def asm_store(tokens):
    slot = int(tokens[1])
    r_src = parse_register(tokens[2])
    slot_bytes = slot.to_bytes(2, "big")
    return bytes([0x37]) + slot_bytes + bytes([r_src])

@register("MLOAD")
def asm_load(tokens):
    r_dst = parse_register(tokens[1])
    slot = parse_register(tokens[2])
    return bytes([0x38, r_dst, slot])

@register("MSTORE")
def asm_store(tokens):
    slot = parse_register(tokens[1])
    r_src = parse_register(tokens[2])
    return bytes([0x39, slot, r_src])




@register("JMP")
def asm_jmp(tokens):
    # JMP position
    pos = int(tokens[1])
    return bytes([0x40]) + pos.to_bytes(4, 'big')


@register("JMPC")
def asm_jmpc(tokens):
    # JMPC rX, position
    r_cond = parse_register(tokens[1])
    pos = int(tokens[2])
    return bytes([0x41, r_cond]) + pos.to_bytes(4, 'big')


@register("END")
def asm_end(tokens):
    return bytes([0x42])



@register("CALLVALUE")
def asm_callvalue(tokens):
    r_dst = parse_register(tokens[1])
    return bytes([0x50, r_dst])

@register("BALANCE")
def asm_balance(tokens):
    r_dst = parse_register(tokens[1])
    return bytes([0x51, r_dst])

@register("TRANSFER")
def asm_transfer(tokens):
    r_address = parse_register(tokens[1])
    r_amount = parse_register(tokens[2])
    return bytes([0x52, r_address, r_amount])

@register("SENDER")
def asm_sender(tokens):
    r_dst = parse_register(tokens[1])
    return bytes([0x53, r_dst])



# === Assembler ===
def assemble_stable(asm_source: str) -> bytes:
    bytecode = bytearray()

    asm_source = asm_source.replace(",", "")

    for line in asm_source.strip().splitlines():
        line = line.strip()
        if not line or line.startswith(";"):
            continue

        tokens = line.split()
        mnemonic = tokens[0].upper()

        if mnemonic not in INSTRUCTION_TABLE:
            raise ValueError(f"Unknown instruction: {mnemonic}")

        instr_bytes = INSTRUCTION_TABLE[mnemonic](tokens)
        bytecode += instr_bytes

    return bytes(bytecode)


def assemble(asm_source: str) -> bytes:
    bytecode = []
    asm_source = asm_source.replace(",", "")
    
    # Etap 1: Wczytaj linie jako tokeny
    for line in asm_source.strip().splitlines():
        line = line.strip()
        if not line or line.startswith(";"):
            continue

        tokens = line.split()
        mnemonic = tokens[0].upper()

        if mnemonic.endswith(":"):
            bytecode.append(["label", mnemonic[:-1]])  # bez ':'
        elif mnemonic not in INSTRUCTION_TABLE:
            raise ValueError(f"Unknown instruction: {mnemonic}")
        elif mnemonic == "JMP":
            bytecode.append(["jump", tokens[1]])
        elif mnemonic == "JMPC":
            bytecode.append(["jumpc", tokens[1], tokens[2]])
        else:
            instr_bytes = INSTRUCTION_TABLE[mnemonic](tokens)
            bytecode.append(["instruction", instr_bytes])

    # Etap 2: Oblicz offsety bajtowe etykiet
    pc = 0
    label_offsets = {}
    for entry in bytecode:
        kind = entry[0]
        if kind == "instruction":
            pc += len(entry[1])
        elif kind == "label":
            label_name = entry[1]
            label_offsets[label_name.lower()] = pc
        elif kind in ("jump", "jumpc"):
            # Skoki mają znaną długość:
            pc += 5 if kind == "jump" else 6

    # Etap 3: Zamień skoki na instrukcje
    final_code = []
    for entry in bytecode:
        kind = entry[0]
        if kind == "instruction":
            final_code.append(entry[1])
        elif kind == "jump":
            label = entry[1]
            if label not in label_offsets:
                raise ValueError(f"Undefined label: {label}")
            offset = label_offsets[label]
            final_code.append(bytes([0x40]) + offset.to_bytes(4, "big"))
        elif kind == "jumpc":
            reg = int(entry[1][1:])  # rX
            label = entry[2]
            if label not in label_offsets:
                raise ValueError(f"Undefined label: {label}")
            offset = label_offsets[label]
            final_code.append(bytes([0x41, reg]) + offset.to_bytes(4, "big"))
        elif kind == "label":
            continue  # pomijamy etykiety w finalnym bajtkodzie

    return b''.join(final_code), label_offsets
