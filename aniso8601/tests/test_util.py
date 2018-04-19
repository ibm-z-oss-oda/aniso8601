# -*- coding: utf-8 -*-

# Copyright (c) 2018, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import unittest

from decimal import Decimal
from aniso8601.util import decimal_split

class TestUtilFunctions(unittest.TestCase):
    def test_decimal_split(self):
        result = decimal_split(Decimal(1))
        self.assertEqual(result, (Decimal(0), Decimal(1)))

        result = decimal_split(Decimal(1.1))
        self.assertAlmostEqual(result[0], Decimal(0.1))
        self.assertEqual(result[1], Decimal(1))

        result = decimal_split(Decimal(2.2))
        self.assertAlmostEqual(result[0], Decimal(0.2))
        self.assertEqual(result[1], Decimal(2))

        result = decimal_split(Decimal(3.3))
        self.assertAlmostEqual(result[0], Decimal(0.3))
        self.assertEqual(result[1], Decimal(3))

        result = decimal_split(Decimal(4.4))
        self.assertAlmostEqual(result[0], Decimal(0.4))
        self.assertEqual(result[1], Decimal(4))

        result = decimal_split(Decimal(5.5))
        self.assertAlmostEqual(result[0], Decimal(0.5))
        self.assertEqual(result[1], Decimal(5))

        result = decimal_split(Decimal(6.6))
        self.assertAlmostEqual(result[0], Decimal(0.6))
        self.assertEqual(result[1], Decimal(6))

        result = decimal_split(Decimal(7.7))
        self.assertAlmostEqual(result[0], Decimal(0.7))
        self.assertEqual(result[1], Decimal(7))

        result = decimal_split(Decimal(8.8))
        self.assertAlmostEqual(result[0], Decimal(0.8))
        self.assertEqual(result[1], Decimal(8))

        result = decimal_split(Decimal(9.9))
        self.assertAlmostEqual(result[0], Decimal(0.9))
        self.assertEqual(result[1], Decimal(9))

        result = decimal_split(Decimal(10.0))
        self.assertAlmostEqual(result[0], Decimal(0))
        self.assertEqual(result[1], Decimal(10))

        result = decimal_split(Decimal(11.1))
        self.assertAlmostEqual(result[0], Decimal(0.1))
        self.assertEqual(result[1], Decimal(11))

        result = decimal_split(Decimal(-1))
        self.assertEqual(result, (Decimal(0), Decimal(-1)))

        result = decimal_split(Decimal(-1.1))
        self.assertAlmostEqual(result[0], Decimal(-0.1))
        self.assertEqual(result[1], Decimal(-1))

        result = decimal_split(Decimal(-2.2))
        self.assertAlmostEqual(result[0], Decimal(-0.2))
        self.assertEqual(result[1], Decimal(-2))

        result = decimal_split(Decimal(-3.3))
        self.assertAlmostEqual(result[0], Decimal(-0.3))
        self.assertEqual(result[1], Decimal(-3))

        result = decimal_split(Decimal(-4.4))
        self.assertAlmostEqual(result[0], Decimal(-0.4))
        self.assertEqual(result[1], Decimal(-4))

        result = decimal_split(Decimal(-5.5))
        self.assertAlmostEqual(result[0], Decimal(-0.5))
        self.assertEqual(result[1], Decimal(-5))

        result = decimal_split(Decimal(-6.6))
        self.assertAlmostEqual(result[0], Decimal(-0.6))
        self.assertEqual(result[1], Decimal(-6))

        result = decimal_split(Decimal(-7.7))
        self.assertAlmostEqual(result[0], Decimal(-0.7))
        self.assertEqual(result[1], Decimal(-7))

        result = decimal_split(Decimal(-8.8))
        self.assertAlmostEqual(result[0], Decimal(-0.8))
        self.assertEqual(result[1], Decimal(-8))

        result = decimal_split(Decimal(-9.9))
        self.assertAlmostEqual(result[0], Decimal(-0.9))
        self.assertEqual(result[1], Decimal(-9))

        result = decimal_split(Decimal(-10.0))
        self.assertAlmostEqual(result[0], Decimal(-0))
        self.assertEqual(result[1], Decimal(-10))

        result = decimal_split(Decimal(-11.1))
        self.assertAlmostEqual(result[0], Decimal(-0.1))
        self.assertEqual(result[1], Decimal(-11))
