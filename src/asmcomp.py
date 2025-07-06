import re
import sys

def parse_register(tok):
    m = re.match(r'r(\d+)$', tok)
    if not m:
        raise ValueError(f"Invalid register '{tok}'")
    reg = int(m.group(1))
    if not (0 <= reg < 2**16):
        raise ValueError(f"Register out of range: {reg}")
    return reg.to_bytes(2, 'big')

# instruction set metadata
INSTRS = {
    'ADD':  {'opc':0x00, 'fmt': ['reg','reg','reg']},
    'SUB':  {'opc':0x01, 'fmt': ['reg','reg','reg']},
    'MUL':  {'opc':0x02, 'fmt': ['reg','reg','reg']},
    'DIV':  {'opc':0x03, 'fmt': ['reg','reg','reg']},
    'MOD':  {'opc':0x04, 'fmt': ['reg','reg','reg']},
    'INC':  {'opc':0x06, 'fmt': ['reg']},
    'DEC':  {'opc':0x07, 'fmt': ['reg']},
    'EQUAL':{'opc':0x10, 'fmt': ['reg','reg','reg']},
    'BIGGER':{'opc':0x11, 'fmt': ['reg','reg','reg']},
    'LOWER':{'opc':0x12, 'fmt': ['reg','reg','reg']},
    'SET4': {'opc':0x20, 'fmt': ['reg','imm',4]},
    'SET8': {'opc':0x21, 'fmt': ['reg','imm',8]},
    'SET16':{'opc':0x22, 'fmt': ['reg','imm',16]},
    'SET20':{'opc':0x23, 'fmt': ['reg','imm',20]},
    'SET':  {'opc':0x24, 'fmt': ['reg','imm',32]},
    'MOV':  {'opc':0x25, 'fmt': ['reg','reg']},
    'STORE':{'opc':0x26, 'fmt': ['key', 'reg']},
    'LOAD': {'opc':0x27, 'fmt': ['reg','key']},
    'FNS':  {'opc':0x30, 'fmt': ['imm',2]},
    'FNE':  {'opc':0x31, 'fmt': []},
    'GOTO': {'opc':0x32, 'fmt': ['imm',2]},
    'IFS':  {'opc':0x33, 'fmt': ['reg']},
    'IFE':  {'opc':0x34, 'fmt': []},
    'END':  {'opc':0x35, 'fmt': []},
}

key_re = re.compile(r"0x([0-9a-fA-F]{64})$")

def parse_key(tok):
    m = key_re.match(tok)
    if not m:
        raise ValueError(f"Invalid key literal '{tok}', expected 64 hex digits prefixed by 0x")
    return bytes.fromhex(m.group(1))


def parse_imm(tok, size):
    # decimal or 0x hex
    if tok.startswith('0x'):
        val = int(tok, 16)
    else:
        val = int(tok)
    b = val.to_bytes(size, 'big')
    if len(b) > size:
        raise ValueError(f"Immediate {tok} too large for {size} bytes")
    return b


def assemble_line(line):
    # strip comments
    code = line.split(';',1)[0].strip()
    if not code:
        return b''
    parts = code.split()
    mnemonic = parts[0].upper()
    if mnemonic not in INSTRS:
        raise ValueError(f"Unknown instruction '{mnemonic}'")
    meta = INSTRS[mnemonic]
    out = bytearray([meta['opc']])
    fmt = meta['fmt']
    i = 1
    for f in fmt:
        if f == 'reg':
            out += parse_register(parts[i])
            i +=1
        elif f == 'imm':
            size = fmt[fmt.index(f)+1]
            out += parse_imm(parts[i], size)
            i +=1
        elif f == 'key':
            out += parse_key(parts[i])
            i +=1
        else:
            # numeric literal size directly
            pass
    return bytes(out)

if __name__ == "__main__":
    # Przykład kodu ASM w zmiennej
    asm_code = [
        "; Definicja funkcji 1",
        "FNS 0x0001",
        "  SET4 r1 10",
        "  SET4 r2 50",
        "  SET4 r3 50",
        "  SET4 r4 50",
        "  ADD  r16 r1 r2",
        "  EQUAL r5 r3 r4",
        "  IFS r5",
        "  GOTO 0x0002",
        "  IFE",
        "FNE",
        "FNS 0x0002",
        "  SET4 r1 50",
        "  SET4 r2 50",
        "  ADD  r16 r1 r2",
        "FNE",
        "",  
        "GOTO 0x0001",
        "END",
    ]

    # Assembler inline: składanie bytecode'u
    byte_chunks = []
    for line in asm_code:
        try:
            chunk = assemble_line(line)
            byte_chunks.append(chunk)
        except ValueError as e:
            print(f"Błąd w asemblerze: {e}")
            sys.exit(1)

    bytecode = b"".join(byte_chunks)

    # Wypisz hex bajty
    hex_repr = bytecode.hex()
    print(f"Assembled bytecode (hex): {hex_repr}")