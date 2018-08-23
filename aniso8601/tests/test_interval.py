# -*- coding: utf-8 -*-

# Copyright (c) 2018, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import unittest

from aniso8601.exceptions import ISOFormatError
from aniso8601.builder import NoneBuilder
from aniso8601.interval import parse_interval, parse_repeating_interval

class TestIntervalParserFunctions(unittest.TestCase):
    def test_parse_interval(self):
        resultinterval = parse_interval('P1M/1981-04-05T01:01:00', builder=NoneBuilder)
        self.assertEqual(resultinterval, (None, (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (None, '1', None, None, None, None, None, 'duration'), 'interval'))

        resultinterval = parse_interval('P1M/1981-04-05', builder=NoneBuilder)
        self.assertEqual(resultinterval, (None, ('1981', '04', '05', None, None, None, 'date'), (None, '1', None, None, None, None, None, 'duration'), 'interval'))

        resultinterval = parse_interval('P1.5Y/2018-03-06', builder=NoneBuilder)
        self.assertEqual(resultinterval, (None, ('2018', '03', '06', None, None, None, 'date'), ('1.5', None, None, None, None, None, None, 'duration'), 'interval'))

        resultinterval = parse_interval('PT1H/2014-11-12', builder=NoneBuilder)
        self.assertEqual(resultinterval, (None, ('2014', '11', '12', None, None, None, 'date'), (None, None, None, None, '1', None, None, 'duration'), 'interval'))

        resultinterval = parse_interval('PT4H54M6.5S/2014-11-12', builder=NoneBuilder)
        self.assertEqual(resultinterval, (None, ('2014', '11', '12', None, None, None, 'date'), (None, None, None, None, '4', '54', '6.5', 'duration'), 'interval'))

        resultinterval = parse_interval('PT0.0000001S/2018-03-06', builder=NoneBuilder)
        self.assertEqual(resultinterval, (None, ('2018', '03', '06', None, None, None, 'date'), (None, None, None, None, None, None, '0.0000001', 'duration'), 'interval'))

        resultinterval = parse_interval('PT2.0000048S/2018-03-06', builder=NoneBuilder)
        self.assertEqual(resultinterval, (None, ('2018', '03', '06', None, None, None, 'date'), (None, None, None, None, None, None, '2.0000048', 'duration'), 'interval'))

        resultinterval = parse_interval('1981-04-05T01:01:00/P1M1DT1M', builder=NoneBuilder)
        self.assertEqual(resultinterval, ((('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, (None, '1', None, '1', None, '1', None, 'duration'), 'interval'))

        resultinterval = parse_interval('1981-04-05/P1M1D', builder=NoneBuilder)
        self.assertEqual(resultinterval, (('1981', '04', '05', None, None, None, 'date'), None, (None, '1', None, '1', None, None, None, 'duration'), 'interval'))

        resultinterval = parse_interval('2018-03-06/P2.5M', builder=NoneBuilder)
        self.assertEqual(resultinterval, (('2018', '03', '06', None, None, None, 'date'), None, (None, '2.5', None, None, None, None, None, 'duration'), 'interval'))

        resultinterval = parse_interval('2014-11-12/PT1H', builder=NoneBuilder)
        self.assertEqual(resultinterval, (('2014', '11', '12', None, None, None, 'date'), None, (None, None, None, None, '1', None, None, 'duration'), 'interval'))

        resultinterval = parse_interval('2014-11-12/PT4H54M6.5S', builder=NoneBuilder)
        self.assertEqual(resultinterval, (('2014', '11', '12', None, None, None, 'date'), None, (None, None, None, None, '4', '54', '6.5', 'duration'), 'interval'))

        resultinterval = parse_interval('2018-03-06/PT0.0000001S', builder=NoneBuilder)
        self.assertEqual(resultinterval, (('2018', '03', '06', None, None, None, 'date'), None, (None, None, None, None, None, None, '0.0000001', 'duration'), 'interval'))

        resultinterval = parse_interval('2018-03-06/PT2.0000048S', builder=NoneBuilder)
        self.assertEqual(resultinterval, (('2018', '03', '06', None, None, None, 'date'), None, (None, None, None, None, None, None, '2.0000048', 'duration'), 'interval'))

        resultinterval = parse_interval('1980-03-05T01:01:00/1981-04-05T01:01:00', builder=NoneBuilder)
        self.assertEqual(resultinterval, ((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, 'interval'))

        resultinterval = parse_interval('1980-03-05T01:01:00/1981-04-05', builder=NoneBuilder)
        self.assertEqual(resultinterval, ((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), ('1981', '04', '05', None, None, None, 'date'), None, 'interval'))

        resultinterval = parse_interval('1980-03-05/1981-04-05T01:01:00', builder=NoneBuilder)
        self.assertEqual(resultinterval, (('1980', '03', '05', None, None, None, 'date'), (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, 'interval'))

        resultinterval = parse_interval('1980-03-05/1981-04-05', builder=NoneBuilder)
        self.assertEqual(resultinterval, (('1980', '03', '05', None, None, None, 'date'), ('1981', '04', '05', None, None, None, 'date'), None, 'interval'))

        resultinterval = parse_interval('1981-04-05/1980-03-05', builder=NoneBuilder)
        self.assertEqual(resultinterval, (('1981', '04', '05', None, None, None, 'date'), ('1980', '03', '05', None, None, None, 'date'), None, 'interval'))

        resultinterval = parse_interval('1980-03-05T01:01:00.0000001/1981-04-05T14:43:59.9999997', builder=NoneBuilder)
        self.assertEqual(resultinterval, ((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00.0000001', None, 'time'), 'datetime'), (('1981', '04', '05', None, None, None, 'date'), ('14', '43', '59.9999997', None, 'time'), 'datetime'), None, 'interval'))

        #Test different separators
        resultinterval = parse_interval('1980-03-05T01:01:00--1981-04-05T01:01:00', intervaldelimiter='--', builder=NoneBuilder)
        self.assertEqual(resultinterval, ((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, 'interval'))

        resultinterval = parse_interval('1980-03-05 01:01:00/1981-04-05 01:01:00', datetimedelimiter=' ', builder=NoneBuilder)
        self.assertEqual(resultinterval, ((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, 'interval'))

    def test_parse_interval_repeating(self):
        #Parse interval can't parse repeating intervals
        with self.assertRaises(ISOFormatError, builder=NoneBuilder):
            parse_interval('R3/1981-04-05/P1D')

        with self.assertRaises(ISOFormatError, builder=NoneBuilder):
            parse_interval('R3/1981-04-05/P0003-06-04T12:30:05.5')

        with self.assertRaises(ISOFormatError, builder=NoneBuilder):
            parse_interval('R/PT1H2M/1980-03-05T01:01:00')

    def test_parse_interval_suffixgarbage(self):
        #Don't allow garbage after the duration
        #https://bitbucket.org/nielsenb/aniso8601/issues/9/durations-with-trailing-garbage-are-parsed
        with self.assertRaises(ValueError):
            parse_interval('2001/P1Dasdf', builder=NoneBuilder)

        with self.assertRaises(ValueError):
            parse_interval('P1Dasdf/2001', builder=NoneBuilder)

        with self.assertRaises(ValueError):
            parse_interval('2001/P0003-06-04T12:30:05.5asdfasdf', builder=NoneBuilder)

        with self.assertRaises(ValueError):
            parse_interval('P0003-06-04T12:30:05.5asdfasdf/2001', builder=NoneBuilder)

class TestRepeatingIntervalParserFunctions(unittest.TestCase):
    def test_parse_repeating_interval(self):
        results = parse_repeating_interval('R3/1981-04-05/P1D', builder=NoneBuilder)
        self.assertEqual(results, (False, '3', (('1981', '04', '05', None, None, None, 'date'), None, (None, None, None, '1', None, None, None, 'duration'), 'interval'), 'repeatinginterval'))

        results = parse_repeating_interval('R11/PT1H2M/1980-03-05T01:01:00', builder=NoneBuilder)
        self.assertEqual(results, (False, '11', (None, (('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (None, None, None, None, '1', '2', None, 'duration'), 'interval'), 'repeatinginterval'))

        results = parse_repeating_interval('R2--1980-03-05T01:01:00--1981-04-05T01:01:00', intervaldelimiter='--', builder=NoneBuilder)
        self.assertEqual(results, (False, '2', ((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, 'interval'), 'repeatinginterval'))

        results = parse_repeating_interval('R2/1980-03-05 01:01:00/1981-04-05 01:01:00', datetimedelimiter=' ', builder=NoneBuilder)
        self.assertEqual(results, (False, '2', ((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, 'interval'), 'repeatinginterval'))

        resultgenerator = parse_repeating_interval('R/PT1H2M/1980-03-05T01:01:00', builder=NoneBuilder)
        self.assertEqual(resultgenerator, (True, None, (None, (('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (None, None, None, None, '1', '2', None, 'duration'), 'interval'), 'repeatinginterval'))

    def test_parse_repeating_interval_suffix_garbage(self):
        #Don't allow garbage after the duration
        #https://bitbucket.org/nielsenb/aniso8601/issues/9/durations-with-trailing-garbage-are-parsed
        with self.assertRaises(ISOFormatError):
            parse_repeating_interval('R3/1981-04-05/P1Dasdf', builder=NoneBuilder)

        with self.assertRaises(ISOFormatError):
            parse_repeating_interval('R3/1981-04-05/P0003-06-04T12:30:05.5asdfasdf', builder=NoneBuilder)
