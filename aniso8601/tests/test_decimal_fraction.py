import unittest

from aniso8601.decimal_fraction import find_separator, split


class TestDecimalFractionFunctions(unittest.TestCase):
    def test_find_separator(self):
        self.assertEqual(find_separator(''), -1)
        self.assertEqual(find_separator('1234'), -1)
        self.assertEqual(find_separator('12.345'), 2)
        self.assertEqual(find_separator('123,45'), 3)

    def test_split(self):
        self.assertEqual(split(''), [''])
        self.assertEqual(split('1'), ['1'])
        self.assertEqual(split('12.34,56'), ['12', '34', '56'])
