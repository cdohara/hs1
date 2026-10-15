"""Tests for the column-major AES states used by 3.py.

Run with: python3 -m unittest -v test_3.py
Known-answer vectors: FIPS 197, Appendix B, round 1.
https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197-upd1.pdf
"""

import importlib.util
from pathlib import Path
import unittest


# Load by path because the implementation's filename starts with a digit.
_spec = importlib.util.spec_from_file_location("aes_part3", Path(__file__).with_name("3.py"))
aes = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(aes)


class ShiftRowTests(unittest.TestCase):
    def test_sequential_state(self):
        # Each group of four consecutive bytes is one column.
        self.assertEqual(
            aes.shiftrow(list(range(16))),
            [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11],
        )

    def test_fips197_round_one(self):
        state = list(bytes.fromhex("d42711aee0bf98f1b8b45de51e415230"))
        expected = list(bytes.fromhex("d4bf5d30e0b452aeb84111f11e2798e5"))
        self.assertEqual(aes.shiftrow(state), expected)

    def test_zero_state(self):
        self.assertEqual(aes.shiftrow([0] * 16), [0] * 16)

    def test_returns_new_list_without_modifying_input(self):
        state = list(range(16))
        original = state.copy()

        result = aes.shiftrow(state)

        self.assertEqual(state, original)
        self.assertIsInstance(result, list)
        self.assertIsNot(result, state)


class MixColumnTests(unittest.TestCase):
    def test_fips197_round_one(self):
        state = list(bytes.fromhex("d4bf5d30e0b452aeb84111f11e2798e5"))
        expected = list(bytes.fromhex("046681e5e0cb199a48f8d37a2806264c"))
        self.assertEqual(aes.mixcolumn(state), expected)

    def test_each_column_is_mixed_independently(self):
        # A single 1 selects one column of the AES multiplication matrix.
        mixed_columns = (
            [2, 1, 1, 3],
            [3, 2, 1, 1],
            [1, 3, 2, 1],
            [1, 1, 3, 2],
        )
        for column in range(4):
            for row, mixed_column in enumerate(mixed_columns):
                with self.subTest(column=column, row=row):
                    state = [0] * 16
                    state[4 * column + row] = 1
                    expected = [0] * 16
                    expected[4 * column:4 * column + 4] = mixed_column

                    self.assertEqual(aes.mixcolumn(state), expected)

    def test_high_bit_reduction(self):
        # Multiplication must reduce modulo x^8 + x^4 + x^3 + x + 1.
        for value, mixed_column in (
            (0x80, [0x1B, 0x80, 0x80, 0x9B]),
            (0xFF, [0xE5, 0xFF, 0xFF, 0x1A]),
        ):
            with self.subTest(value=value):
                state = [value, 0, 0, 0] + [0] * 12
                self.assertEqual(aes.mixcolumn(state), mixed_column + [0] * 12)

    def test_zero_state(self):
        self.assertEqual(aes.mixcolumn([0] * 16), [0] * 16)

    def test_returns_new_list_without_modifying_input(self):
        state = list(range(16))
        original = state.copy()

        result = aes.mixcolumn(state)

        self.assertEqual(state, original)
        self.assertIsInstance(result, list)
        self.assertIsNot(result, state)


if __name__ == "__main__":
    unittest.main()
