# -*- coding: utf-8 -*-

# Copyright (c) 2018, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import unittest

from decimal import Decimal
from aniso8601.util import decimal_split, decimal_truncate

class TestUtilFunctions(unittest.TestCase):
    def test_decimal_split(self):
        result = decimal_split(Decimal(1))
        self.assertEqual(result, (Decimal(0), Decimal(1)))

        result = decimal_split(Decimal('1.1'))
        self.assertEqual(result, (Decimal('0.1'), Decimal(1)))

        result = decimal_split(Decimal('2.2'))
        self.assertEqual(result, (Decimal('0.2'), Decimal(2)))

        result = decimal_split(Decimal('3.3'))
        self.assertEqual(result, (Decimal('0.3'), Decimal(3)))

        result = decimal_split(Decimal('4.4'))
        self.assertEqual(result, (Decimal('0.4'), Decimal(4)))

        result = decimal_split(Decimal('5.5'))
        self.assertEqual(result, (Decimal('0.5'), Decimal(5)))

        result = decimal_split(Decimal('6.6'))
        self.assertEqual(result, (Decimal('0.6'), Decimal(6)))

        result = decimal_split(Decimal('7.7'))
        self.assertEqual(result, (Decimal('0.7'), Decimal(7)))

        result = decimal_split(Decimal('8.8'))
        self.assertEqual(result, (Decimal('0.8'), Decimal(8)))

        result = decimal_split(Decimal('9.9'))
        self.assertEqual(result, (Decimal('0.9'), Decimal(9)))

        result = decimal_split(Decimal('10.0'))
        self.assertEqual(result, (Decimal(0), Decimal(10)))

        result = decimal_split(Decimal('11.1'))
        self.assertEqual(result, (Decimal('0.1'), Decimal(11)))

        result = decimal_split(Decimal(-1))
        self.assertEqual(result, (Decimal(0), Decimal(-1)))

        result = decimal_split(Decimal('-1.1'))
        self.assertEqual(result, (Decimal('-0.1'), Decimal(-1)))

        result = decimal_split(Decimal('-2.2'))
        self.assertEqual(result, (Decimal('-0.2'), Decimal(-2)))

        result = decimal_split(Decimal('-3.3'))
        self.assertEqual(result, (Decimal('-0.3'), Decimal(-3)))

        result = decimal_split(Decimal('-4.4'))
        self.assertEqual(result, (Decimal('-0.4'), Decimal(-4)))

        result = decimal_split(Decimal('-5.5'))
        self.assertEqual(result, (Decimal('-0.5'), Decimal(-5)))

        result = decimal_split(Decimal('-6.6'))
        self.assertEqual(result, (Decimal('-0.6'), Decimal(-6)))

        result = decimal_split(Decimal('-7.7'))
        self.assertEqual(result, (Decimal('-0.7'), Decimal(-7)))

        result = decimal_split(Decimal('-8.8'))
        self.assertEqual(result, (Decimal('-0.8'), Decimal(-8)))

        result = decimal_split(Decimal('-9.9'))
        self.assertEqual(result, (Decimal('-0.9'), Decimal(-9)))

        result = decimal_split(Decimal('-10.0'))
        self.assertEqual(result, (Decimal(0), Decimal(-10)))

        result = decimal_split(Decimal('-11.1'))
        self.assertEqual(result, (Decimal('-0.1'), Decimal(-11)))

    def test_decimal_truncate(self):
        result = decimal_truncate(Decimal(0), 1)
        self.assertEqual(result, Decimal(0))

        result = decimal_truncate(Decimal(1), 2)
        self.assertEqual(result, Decimal(1))

        result = decimal_truncate(Decimal('1.234'), 3)
        self.assertEqual(result, Decimal('1.234'))

        result = decimal_truncate(Decimal('1.234'), 2)
        self.assertEqual(result, Decimal('1.23'))

        result = decimal_truncate(Decimal('.123'), 1)
        self.assertEqual(result, Decimal('0.1'))

        result = decimal_truncate(Decimal(-1), 2)
        self.assertEqual(result, Decimal(-1))

        result = decimal_truncate(Decimal('-1.234'), 3)
        self.assertEqual(result, Decimal('-1.234'))

        result = decimal_truncate(Decimal('-1.234'), 2)
        self.assertEqual(result, Decimal('-1.23'))

        result = decimal_truncate(Decimal('-.123'), 1)
        self.assertEqual(result, Decimal('-0.1'))
