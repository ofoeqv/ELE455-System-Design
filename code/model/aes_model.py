"""Readable AES-128 teaching model, following FIPS 197.

State is a flat list in column order: state[4*column + row].
This is a functional reference, not constant-time production cryptography.
"""
import argparse

def xtime(a):
    """Multiply a byte by x in GF(2^8), reducing by x^8+x^4+x^3+x+1."""
    return ((a << 1) ^ (0x1B if a & 0x80 else 0)) & 0xFF

def gf_mul(a, b):
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        a = xtime(a)
        b >>= 1
    return result

def _sbox_byte(a):
    inverse = 0
    if a:
        inverse = 1
        for _ in range(254):
            inverse = gf_mul(inverse, a)
    def rot(x, n):
        return ((x << n) | (x >> (8-n))) & 255
    return inverse ^ rot(inverse, 1) ^ rot(inverse, 2) ^ rot(inverse, 3) ^ rot(inverse, 4) ^ 0x63

SBOX = tuple(_sbox_byte(a) for a in range(256))
_inv = [0] * 256
for _a, _b in enumerate(SBOX):
    _inv[_b] = _a
INV_SBOX = tuple(_inv)

def block(value):
    result = list(value)
    if len(result) != 16 or any(not isinstance(x, int) or not 0 <= x < 256 for x in result):
        raise ValueError("Expected exactly 16 byte values")
    return result

def add_round_key(state, key):
    return [a ^ b for a, b in zip(block(state), block(key))]

def sub_bytes(state, inverse=False):
    table = INV_SBOX if inverse else SBOX
    return [table[x] for x in block(state)]

def shift_rows(state, inverse=False):
    state = block(state)
    direction = -1 if inverse else 1
    return [state[4*((c + direction*r) % 4) + r] for c in range(4) for r in range(4)]

def mix_columns(state, inverse=False):
    state = block(state)
    matrix = ((14,11,13,9),(9,14,11,13),(13,9,14,11),(11,13,9,14)) if inverse else (
        (2,3,1,1),(1,2,3,1),(1,1,2,3),(3,1,1,2))
    output = []
    for c in range(4):
        column = state[4*c:4*c+4]
        for row in matrix:
            value = 0
            for coefficient, byte in zip(row, column):
                value ^= gf_mul(coefficient, byte)
            output.append(value)
    return output

def expand_key(key):
    words = [block(key)[i:i+4] for i in range(0,16,4)]
    rcon = 1
    for i in range(4,44):
        temp = words[i-1][:]
        if i % 4 == 0:
            temp = [SBOX[x] for x in temp[1:] + temp[:1]]
            temp[0] ^= rcon
            rcon = xtime(rcon)
        words.append([a ^ b for a,b in zip(words[i-4], temp)])
    return [sum(words[4*r:4*r+4], []) for r in range(11)]

def encrypt(plaintext, key, trace=None):
    keys = expand_key(key)
    state = block(plaintext)
    def record(label):
        if trace is not None:
            trace.append((label, bytes(state)))
    record("input")
    state = add_round_key(state, keys[0]); record("r0.add_round_key")
    for r in range(1,11):
        state = sub_bytes(state); record(f"r{r}.sub_bytes")
        state = shift_rows(state); record(f"r{r}.shift_rows")
        if r != 10:
            state = mix_columns(state); record(f"r{r}.mix_columns")
        state = add_round_key(state, keys[r]); record(f"r{r}.add_round_key")
    return bytes(state)

def decrypt(ciphertext, key):
    keys = expand_key(key)
    state = add_round_key(ciphertext, keys[10])
    for r in range(9,0,-1):
        state = shift_rows(state, inverse=True)
        state = sub_bytes(state, inverse=True)
        state = add_round_key(state, keys[r])
        state = mix_columns(state, inverse=True)
    state = shift_rows(state, inverse=True)
    state = sub_bytes(state, inverse=True)
    return bytes(add_round_key(state, keys[0]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--plaintext", default="00112233445566778899aabbccddeeff")
    parser.add_argument("--key", default="000102030405060708090a0b0c0d0e0f")
    parser.add_argument("--trace", action="store_true")
    args = parser.parse_args()
    records = []
    ciphertext = encrypt(bytes.fromhex(args.plaintext), bytes.fromhex(args.key), records)
    if args.trace:
        for label, value in records:
            print(f"{label:20} {value.hex()}")
    print("ciphertext", ciphertext.hex())
    print("recovered ", decrypt(ciphertext, bytes.fromhex(args.key)).hex())
