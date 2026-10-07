"""Run with python -m unittest discover -s model -v from code/."""
import random
import unittest
from aes_model import *

class ModelTests(unittest.TestCase):
    def test_published_vectors(self):
        vectors = [
            ("000102030405060708090a0b0c0d0e0f", "00112233445566778899aabbccddeeff",
             "69c4e0d86a7b0430d8cdb78070b4c55a"),
            ("2b7e151628aed2a6abf7158809cf4f3c", "6bc1bee22e409f96e93d7e117393172a",
             "3ad77bb40d7a3660a89ecaf32466ef97"),
            ("2b7e151628aed2a6abf7158809cf4f3c", "ae2d8a571e03ac9c9eb76fac45af8e51",
             "f5d3d58503b9699de785895a96fdbaaf"),
            ("2b7e151628aed2a6abf7158809cf4f3c", "30c81c46a35ce411e5fbc1191a0a52ef",
             "43b1cd7f598ece23881b00e3ed030688"),
            ("2b7e151628aed2a6abf7158809cf4f3c", "f69f2445df4f9b17ad2b417be66c3710",
             "7b0c785e27e8ad3f8223207104725dd4"),
        ]
        for k,p,c in vectors:
            key, plain, cipher = map(bytes.fromhex, (k,p,c))
            self.assertEqual(encrypt(plain,key), cipher)
            self.assertEqual(decrypt(cipher,key), plain)

    def test_trace_and_key(self):
        key = bytes(range(16)); records = []
        encrypt(bytes.fromhex("00112233445566778899aabbccddeeff"), key, records)
        trace = dict(records)
        expected = {
            "r0.add_round_key":"00102030405060708090a0b0c0d0e0f0",
            "r1.sub_bytes":"63cab7040953d051cd60e0e7ba70e18c",
            "r1.shift_rows":"6353e08c0960e104cd70b751bacad0e7",
            "r1.mix_columns":"5f72641557f5bc92f7be3b291db9f91a",
            "r1.add_round_key":"89d810e8855ace682d1843d8cb128fe4",
        }
        for label,value in expected.items():
            self.assertEqual(trace[label].hex(), value)
        self.assertEqual(bytes(expand_key(key)[1]).hex(), "d6aa74fdd2af72fadaa678f1d6ab76fe")
        self.assertNotIn("r10.mix_columns", trace)

    def test_properties(self):
        rng = random.Random(455)
        self.assertEqual(SBOX[0x53],0xed)
        self.assertEqual(xtime(0x57),0xae)
        self.assertEqual(xtime(0x83),0x1d)
        self.assertEqual(len(set(SBOX)),256)
        for a in range(256):
            self.assertEqual(INV_SBOX[SBOX[a]],a)
        for _ in range(30):
            state = [rng.randrange(256) for _ in range(16)]
            key = bytes(rng.randrange(256) for _ in range(16))
            self.assertEqual(shift_rows(shift_rows(state), True), state)
            self.assertEqual(mix_columns(mix_columns(state), True), state)
            self.assertEqual(decrypt(encrypt(state,key),key),bytes(state))

    def test_bad_input(self):
        for bad in [[], [0]*15, [0]*17, [256]*16]:
            with self.assertRaises(ValueError):
                encrypt(bad, bytes(16))

if __name__ == "__main__":
    unittest.main()
