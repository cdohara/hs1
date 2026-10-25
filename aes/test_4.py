"""S-box and AES-128 key-expansion tests for 4.py.

Run with: python3 -m unittest -v test_4.py
keyschedule() is expected to return 44 32-bit words (w0 through w43),
with the input key read most-significant word first.
Reference: FIPS 197, Table 4 and Appendix A.1.
https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197-upd1.pdf
"""

import importlib.util
from pathlib import Path
import unittest


_spec = importlib.util.spec_from_file_location("aes_part4", Path(__file__).with_name("4.py"))
aes = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(aes)


# Original key followed by the ten round keys from Appendix A.1.
EXPECTED_ROUND_KEYS = (
    "2B7E151628AED2A6ABF7158809CF4F3C",
    "A0FAFE1788542CB123A339392A6C7605",
    "F2C295F27A96B9435935807A7359F67F",
    "3D80477D4716FE3E1E237E446D7A883B",
    "EF44A541A8525B7FB671253BDB0BAD00",
    "D4D1C6F87C839D87CAF2B8BC11F915BC",
    "6D88A37A110B3EFDDBF98641CA0093FD",
    "4E54F70E5F5FC9F384A64FB24EA6DC4F",
    "EAD27321B58DBAD2312BF5607F8D292F",
    "AC7766F319FADC2128D12941575C006E",
    "D014F9A8C9EE2589E13F0CC8B6630CA6",
)
SBOX_CASES = ((0x00, 0x63), (0x53, 0xED), (0xC2, 0x25), (0xFF, 0x16))


class SboxTests(unittest.TestCase):
    def test_getsub_known_bytes(self):
        for value, expected in SBOX_CASES:
            with self.subTest(byte=f"{value:02X}"):
                self.assertEqual(aes.getsub(value >> 4, value & 0x0F), expected)

    def test_subkey_known_bytes(self):
        for value, expected in SBOX_CASES:
            with self.subTest(byte=f"{value:02X}"):
                result = aes.subkey(value)
                self.assertEqual(result, expected)


class KeyScheduleTests(unittest.TestCase):
    def test_aes128_round_one_key_expansion(self):
        key = 0x2B7E151628AED2A6ABF7158809CF4F3C
        expected = "A0FAFE1788542CB123A339392A6C7605"
        expanded = aes.keyschedule(key)
        # Words 0-3 contain the original key; words 4-7 form round 1.
        round_one_key = "".join(f"{word:08x}" for word in expanded[4:8])
        passed = round_one_key.upper() == expected
        separator = "-" * 64
        print(
            f"\n{separator}\n"
            "AES-128 KEY EXPANSION TEST\n"
            f"{separator}\n"
            f"Original Key = {key:032x}\n"
            f"Round 1 Key  = {round_one_key}\n"
            f"Expected     = {expected}\n"
            f"KEY EXPANSION {'PASS' if passed else 'FAIL'}",
            flush=True,
        )
        self.assertEqual(round_one_key.upper(), expected, "Round 1 key does not match")

    def test_fips197_full_schedule(self):
        key = int(EXPECTED_ROUND_KEYS[0], 16)
        expected = [
            int(round_key[offset:offset + 8], 16)
            for round_key in EXPECTED_ROUND_KEYS
            for offset in range(0, 32, 8)
        ]
        result = aes.keyschedule(key)
        print(f"\nKEYSCHEDULE VERIFICATION:\nInput key    : {key:032X}", flush=True)
        if isinstance(result, list):
            for round_number, expected_hex in enumerate(EXPECTED_ROUND_KEYS):
                words = result[4 * round_number:4 * round_number + 4]
                actual_hex = "".join(f"{word:08X}" for word in words)
                print(
                    f"Round {round_number:02d}     : {actual_hex}\n"
                    f"Expected     : {expected_hex}",
                    flush=True,
                )
        else:
            print(f"Output       : {result!r}", flush=True)
            print("Expected     : 44 words (11 round keys)", flush=True)
        print(f"Result       : {'PASS' if result == expected else 'FAIL'}", flush=True)
        self.assertEqual(result, expected, "Expanded key must match FIPS 197 Appendix A.1")

    def test_zero_key_first_round(self):
        # S(00) = 63; XOR with the first round constant gives 62636363.
        result = aes.keyschedule(0)
        self.assertIsInstance(result, list, "keyschedule() must return the expanded words")
        self.assertEqual(len(result), 44, "AES-128 needs 44 expanded words")
        self.assertEqual(result[:8], [0] * 4 + [0x62636363] * 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
