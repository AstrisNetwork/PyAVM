import hashlib
import json


# === Code Loader ===
class Code:
    def __init__(self, byte_code: bytes):
        self.byte_code = byte_code
        self.offset = 0

    def read_byte(self) -> int:
        val = self.byte_code[self.offset]
        self.offset += 1
        return val

    def read_bytes(self, count: int) -> bytes:
        val = self.byte_code[self.offset:self.offset + count]
        self.offset += count
        return val



def bytes32_to_int(b: bytes) -> int:
    if len(b) != 32:
        raise ValueError("Expected 32 bytes")
    return int.from_bytes(b, byteorder="big", signed=True)

def int_to_bytes32(i: int) -> bytes:
    return i.to_bytes(32, byteorder="big", signed=True)

def get_abi_hash(abi: dict) -> bytes:
    # Sortujemy i zamieniamy na string, by uzyskać stabilny hash
    abi_str = json.dumps(abi, separators=(",", ":"), sort_keys=True)
    abi_hash = hashlib.sha3_256(abi_str.encode()).digest()

    return abi_hash