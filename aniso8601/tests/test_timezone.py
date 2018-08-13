# -*- coding: utf-8 -*-

# Copyright (c) 2018, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import unittest
import datetime

from aniso8601.builder import NoneBuilder
from aniso8601.exceptions import ISOFormatError
from aniso8601.timezone import parse_timezone

class TestTimezoneParserFunctions(unittest.TestCase):
    def test_parse_timezone(self):
        parse = parse_timezone('Z', builder=NoneBuilder)
        self.assertEqual(parse, (False, True, None, None, 'Z'))

        parse = parse_timezone('+00:00', builder=NoneBuilder)
        self.assertEqual(parse, (False, None, '00', '00', '+00:00'))

        parse = parse_timezone('+01:00', builder=NoneBuilder)
        self.assertEqual(parse, (False, None, '01', '00', '+01:00'))

        parse = parse_timezone('-01:00', builder=NoneBuilder)
        self.assertEqual(parse, (True, None, '01', '00', '-01:00'))

        parse = parse_timezone('+00:12', builder=NoneBuilder)
        self.assertEqual(parse, (False, None, '00', '12', '+00:12'))

        parse = parse_timezone('+01:23', builder=NoneBuilder)
        self.assertEqual(parse, (False, None, '01', '23', '+01:23'))

        parse = parse_timezone('-01:23', builder=NoneBuilder)
        self.assertEqual(parse, (True, None, '01', '23', '-01:23'))

        parse = parse_timezone('+0000', builder=NoneBuilder)
        self.assertEqual(parse, (False, None, '00', '00', '+0000'))

        parse = parse_timezone('+0100', builder=NoneBuilder)
        self.assertEqual(parse, (False, None, '01', '00', '+0100'))

        parse = parse_timezone('-0100', builder=NoneBuilder)
        self.assertEqual(parse, (True, None, '01', '00', '-0100'))

        parse = parse_timezone('+0012', builder=NoneBuilder)
        self.assertEqual(parse, (False, None, '00', '12', '+0012'))

        parse = parse_timezone('+0123', builder=NoneBuilder)
        self.assertEqual(parse, (False, None, '01', '23', '+0123'))

        parse = parse_timezone('-0123', builder=NoneBuilder)
        self.assertEqual(parse, (True, None, '01', '23', '-0123'))

        parse = parse_timezone('+00', builder=NoneBuilder)
        self.assertEqual(parse, (False, None, '00', None, '+00'))

        parse = parse_timezone('+01', builder=NoneBuilder)
        self.assertEqual(parse, (False, None, '01', None, '+01'))

        parse = parse_timezone('-01', builder=NoneBuilder)
        self.assertEqual(parse, (True, None, '01', None, '-01'))

        parse = parse_timezone('+12', builder=NoneBuilder)
        self.assertEqual(parse, (False, None, '12', None, '+12'))

        parse = parse_timezone('-12', builder=NoneBuilder)
        self.assertEqual(parse, (True, None, '12', None, '-12'))

    def test_parse_timezone_tzstr(self):
        with self.assertRaises(ISOFormatError):
            parse_timezone('Y', builder=NoneBuilder)

        with self.assertRaises(ISOFormatError):
            parse_timezone(' Z', builder=NoneBuilder)

        with self.assertRaises(ISOFormatError):
            parse_timezone('Z ', builder=NoneBuilder)

        with self.assertRaises(ISOFormatError):
            parse_timezone(' Z ', builder=NoneBuilder)

    def test_parse_timezone_negativezero(self):
        #A 0 offset cannot be negative
        with self.assertRaises(ISOFormatError, builder=NoneBuilder):
            parse_timezone('-00:00')

        with self.assertRaises(ISOFormatError, builder=NoneBuilder):
            parse_timezone('-0000')

        with self.assertRaises(ISOFormatError, builder=NoneBuilder):
            parse_timezone('-00')
