"""Run from code/: python model/explore_preparation.py 1 (or 2 or 3)."""
import argparse
from aes_model import (encrypt, decrypt, expand_key, add_round_key,
                       shift_rows, sub_bytes, mix_columns, xtime)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('week', type=int, choices=[1, 2, 3])
    week = parser.parse_args().week
    plaintext = bytes.fromhex('00112233445566778899aabbccddeeff')
    key = bytes.fromhex('000102030405060708090a0b0c0d0e0f')
    if week == 1:
        for row in range(4):
            print('row', row, [f'{plaintext[4*col+row]:02x}' for col in range(4)])
        print('initial key addition', bytes(add_round_key(plaintext, key)).hex())
        assert bytes(add_round_key(plaintext, key)).hex() == '00102030405060708090a0b0c0d0e0f0'
    elif week == 2:
        print('ShiftRows', bytes(shift_rows(bytes(range(16)))).hex())
        print('S-box 53', f'{sub_bytes([0x53]*16)[0]:02x}')
        print('xtime 57 / 83', f'{xtime(0x57):02x}', f'{xtime(0x83):02x}')
        column = [0xdb, 0x13, 0x53, 0x45]
        mixed = mix_columns(column + [0]*12)
        print('MixColumns', bytes(mixed[:4]).hex())
        assert mixed[:4] == [0x8e, 0x4d, 0xa1, 0xbc]
    else:
        trace = []
        ciphertext = encrypt(plaintext, key, trace)
        for label, state in trace:
            print(label, state.hex())
        print('round keys', len(expand_key(key)))
        assert ciphertext.hex() == '69c4e0d86a7b0430d8cdb78070b4c55a'
        assert decrypt(ciphertext, key) == plaintext
        labels = [label for label, _ in trace]
        assert 'r9.mix_columns' in labels and 'r10.mix_columns' not in labels

if __name__ == '__main__':
    main()
