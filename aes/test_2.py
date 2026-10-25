"""S-box tests for 2.py; bit-list inputs are most-significant bit first.

Run with: python3 -m unittest -v test_2.py
Reference: FIPS 197, Table 4 and Appendix B, round 1.
https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197-upd1.pdf
"""

import importlib.util
from pathlib import Path
import unittest


_spec = importlib.util.spec_from_file_location("aes_part2", Path(__file__).with_name("2.py"))
aes = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(aes)


# Fixed reference data, independent of the implementation's lookup table.
EXPECTED_SBOX = bytes.fromhex(
    "637c777bf26b6fc53001672bfed7ab76"
    "ca82c97dfa5947f0add4a2af9ca472c0"
    "b7fd9326363ff7cc34a5e5f171d83115"
    "04c723c31896059a071280e2eb27b275"
    "09832c1a1b6e5aa0523bd6b329e32f84"
    "53d100ed20fcb15b6acbbe394a4c58cf"
    "d0efaafb434d338545f9027f503c9fa8"
    "51a3408f929d38f5bcb6da2110fff3d2"
    "cd0c13ec5f974417c4a77e3d645d1973"
    "60814fdc222a908846eeb814de5e0bdb"
    "e0323a0a4906245cc2d3ac629195e479"
    "e7c8376d8dd54ea96c56f4ea657aae08"
    "ba78252e1ca6b4c6e8dd741f4bbd8b8a"
    "703eb5664803f60e613557b986c11d9e"
    "e1f8981169d98e949b1e87e9ce5528df"
    "8ca1890dbfe6426841992d0fb054bb16"
)


def _bits(value):
    return [int(bit) for bit in f"{value:08b}"]


def _print_verification(name, state, result, expected):
    print(
        f"\n{name} VERIFICATION:\n"
        f"Input        : {state.hex().upper()}\n"
        f"Output       : {result.hex().upper()}\n"
        f"Expected     : {expected.hex().upper()}\n"
        f"Result       : {'PASS' if result == expected else 'FAIL'}",
        flush=True,
    )


class SboxTests(unittest.TestCase):
    def test_getsub_all_256_bytes(self):
        for value, expected in enumerate(EXPECTED_SBOX):
            with self.subTest(byte=f"{value:02X}"):
                self.assertEqual(aes.getsub(value >> 4, value & 0x0F), expected)

    def test_subkey_all_256_bit_inputs(self):
        for value, expected in enumerate(EXPECTED_SBOX):
            with self.subTest(byte=f"{value:02X}"):
                self.assertEqual(aes.subkey(_bits(value)), expected)

    def test_c2_example(self):
        result = aes.subkey(_bits(0xC2))
        _print_verification("SBOX C2", bytes([0xC2]), bytes([result]), bytes([0x25]))
        self.assertEqual(result, 0x25)

    def test_fips197_subbytes_round_one(self):
        state = bytes.fromhex("193DE3BEA0F4E22B9AC68D2AE9F84808")
        expected = bytes.fromhex("D42711AEE0BF98F1B8B45DE51E415230")
        result = bytes(aes.subkey(_bits(value)) for value in state)
        _print_verification("SUBBYTES", state, result, expected)
        self.assertEqual(result, expected)

    def test_subkey_does_not_modify_bit_input(self):
        state = _bits(0xC2)
        original = state.copy()
        aes.subkey(state)
        self.assertEqual(state, original)


if __name__ == "__main__":
    unittest.main(verbosity=2)
