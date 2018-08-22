# -*- coding: utf-8 -*-

# Copyright (c) 2018, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import unittest
import datetime
import dateutil.relativedelta

from aniso8601 import compat
from aniso8601.exceptions import ISOFormatError, RelativeValueError
from aniso8601.builder import NoneBuilder
from aniso8601.interval import parse_interval, parse_repeating_interval, _parse_interval

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

class TestRelativeIntervalParserFunctions(unittest.TestCase):
    def test_parse_interval_relative(self):
        resultinterval = parse_interval('P1M/1981-04-05T01:01:00', relative=True)
        self.assertEqual(resultinterval[0], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))
        self.assertEqual(resultinterval[1], datetime.datetime(year=1981, month=3, day=5, hour=1, minute=1))

        resultinterval = parse_interval('P1M/1981-04-05', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=1981, month=4, day=5))
        self.assertEqual(resultinterval[1], datetime.date(year=1981, month=3, day=5))

        resultinterval = parse_interval('PT1H/2014-11-12', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=2014, month=11, day=12))
        self.assertEqual(resultinterval[1], datetime.datetime(year=2014, month=11, day=11, hour=23))

        resultinterval = parse_interval('PT4H54M6.5S/2014-11-12', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=2014, month=11, day=12))
        self.assertEqual(resultinterval[1], datetime.datetime(year=2014, month=11, day=11, hour=19, minute=5, second=53, microsecond=500000))

        #Make sure we truncate, not round
        #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
        resultinterval = parse_interval('PT0.0000001S/2018-03-06', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=2018, month=3, day=6))
        self.assertEqual(resultinterval[1], datetime.datetime(year=2018, month=3, day=6))

        resultinterval = parse_interval('PT2.0000048S/2018-03-06', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=2018, month=3, day=6))
        self.assertEqual(resultinterval[1], datetime.datetime(year=2018, month=3, day=5, hour=23, minute=59, second=57, microsecond=999996))

        resultinterval = parse_interval('1981-04-05T01:01:00/P1M1DT1M', relative=True)
        self.assertEqual(resultinterval[0], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))
        self.assertEqual(resultinterval[1], datetime.datetime(year=1981, month=5, day=6, hour=1, minute=2))

        resultinterval = parse_interval('1981-04-05/P1M1D', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=1981, month=4, day=5))
        self.assertEqual(resultinterval[1], datetime.date(year=1981, month=5, day=6))

        resultinterval = parse_interval('2014-11-12/PT1H', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=2014, month=11, day=12))
        self.assertEqual(resultinterval[1], datetime.datetime(year=2014, month=11, day=12, hour=1, minute=0))

        resultinterval = parse_interval('2014-11-12/PT4H54M6.5S', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=2014, month=11, day=12))
        self.assertEqual(resultinterval[1], datetime.datetime(year=2014, month=11, day=12, hour=4, minute=54, second=6, microsecond=500000))

        #Some relativedelta examples
        #http://dateutil.readthedocs.org/en/latest/examples.html#relativedelta-examples
        resultinterval = parse_interval('2003-01-27/P1M', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=2003, month=1, day=27))
        self.assertEqual(resultinterval[1], datetime.date(year=2003, month=2, day=27))

        resultinterval = parse_interval('2003-01-31/P1M', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=2003, month=1, day=31))
        self.assertEqual(resultinterval[1], datetime.date(year=2003, month=2, day=28))

        resultinterval = parse_interval('2003-01-31/P2M', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=2003, month=1, day=31))
        self.assertEqual(resultinterval[1], datetime.date(year=2003, month=3, day=31))

        resultinterval = parse_interval('2000-02-28/P1Y', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=2000, month=2, day=28))
        self.assertEqual(resultinterval[1], datetime.date(year=2001, month=2, day=28))

        resultinterval = parse_interval('1999-02-28/P1Y', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=1999, month=2, day=28))
        self.assertEqual(resultinterval[1], datetime.date(year=2000, month=2, day=28))

        resultinterval = parse_interval('1999-03-01/P1Y', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=1999, month=3, day=1))
        self.assertEqual(resultinterval[1], datetime.date(year=2000, month=3, day=1))

        resultinterval = parse_interval('P1Y/2001-02-28', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=2001, month=2, day=28))
        self.assertEqual(resultinterval[1], datetime.date(year=2000, month=2, day=28))

        resultinterval = parse_interval('P1Y/2001-03-01', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=2001, month=3, day=1))
        self.assertEqual(resultinterval[1], datetime.date(year=2000, month=3, day=1))

        #Make sure we truncate, not round
        #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
        resultinterval = parse_interval('2018-03-06/PT0.0000001S', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=2018, month=3, day=6))
        self.assertEqual(resultinterval[1], datetime.datetime(year=2018, month=3, day=6))

        resultinterval = parse_interval('2018-03-06/PT2.0000048S', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=2018, month=3, day=6))
        self.assertEqual(resultinterval[1], datetime.datetime(year=2018, month=3, day=6, hour=0, minute=0, second=2, microsecond=4))

        resultinterval = parse_interval('1980-03-05T01:01:00/1981-04-05T01:01:00', relative=True)
        self.assertEqual(resultinterval[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(resultinterval[1], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))

        resultinterval = parse_interval('1980-03-05T01:01:00/1981-04-05', relative=True)
        self.assertEqual(resultinterval[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(resultinterval[1], datetime.date(year=1981, month=4, day=5))

        resultinterval = parse_interval('1980-03-05/1981-04-05T01:01:00', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=1980, month=3, day=5))
        self.assertEqual(resultinterval[1], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))

        resultinterval = parse_interval('1980-03-05/1981-04-05', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=1980, month=3, day=5))
        self.assertEqual(resultinterval[1], datetime.date(year=1981, month=4, day=5))

        resultinterval = parse_interval('1981-04-05/1980-03-05', relative=True)
        self.assertEqual(resultinterval[0], datetime.date(year=1981, month=4, day=5))
        self.assertEqual(resultinterval[1], datetime.date(year=1980, month=3, day=5))

        #Make sure we truncate, not round
        #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
        resultinterval = parse_interval('1980-03-05T01:01:00.0000001/1981-04-05T14:43:59.9999997', relative=True)
        self.assertEqual(resultinterval[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(resultinterval[1], datetime.datetime(year=1981, month=4, day=5, hour=14, minute=43, second=59, microsecond=999999))

        #Test different separators
        resultinterval = parse_interval('1980-03-05T01:01:00--1981-04-05T01:01:00', intervaldelimiter='--', relative=True)
        self.assertEqual(resultinterval[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(resultinterval[1], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))

        resultinterval = parse_interval('1980-03-05 01:01:00/1981-04-05 01:01:00', datetimedelimiter=' ', relative=True)
        self.assertEqual(resultinterval[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(resultinterval[1], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))

    def test_parse_interval_relative_fractionalyear(self):
        #Fractional months and years are not defined
        #https://github.com/dateutil/dateutil/issues/40
        with self.assertRaises(RelativeValueError):
            parse_interval('P1.5Y/2018-03-06', relative=True)

    def test_parse_interval_relative_fractionalmonth(self):
        #Fractional months and years are not defined
        #https://github.com/dateutil/dateutil/issues/40
        with self.assertRaises(RelativeValueError):
            parse_interval('2018-03-06/P2.5M', relative=True)

    def test_parse_interval_relative_suffixgarbage(self):
        #Don't allow garbage after the duration
        #https://bitbucket.org/nielsenb/aniso8601/issues/9/durations-with-trailing-garbage-are-parsed
        with self.assertRaises(ValueError):
            parse_interval('2001/P1Dasdf', relative=True)

        with self.assertRaises(ValueError):
            parse_interval('P1Dasdf/2001', relative=True)

        with self.assertRaises(ValueError):
            parse_interval('2001/P0003-06-04T12:30:05.5asdfasdf', relative=True)

        with self.assertRaises(ValueError):
            parse_interval('P0003-06-04T12:30:05.5asdfasdf/2001', relative=True)

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

    def test_parse_repeating_interval_suffixgarbage(self):
        #Don't allow garbage after the duration
        #https://bitbucket.org/nielsenb/aniso8601/issues/9/durations-with-trailing-garbage-are-parsed
        with self.assertRaises(ISOFormatError):
            parse_repeating_interval('R3/1981-04-05/P1Dasdf', builder=NoneBuilder)

        with self.assertRaises(ISOFormatError):
            parse_repeating_interval('R3/1981-04-05/P0003-06-04T12:30:05.5asdfasdf', builder=NoneBuilder)

    def test_parse_repeating_interval_relative(self):
        results = list(parse_repeating_interval('R3/1981-04-05/P1D', relative=True))
        self.assertEqual(results[0], datetime.date(year=1981, month=4, day=5))
        self.assertEqual(results[1], datetime.date(year=1981, month=4, day=6))
        self.assertEqual(results[2], datetime.date(year=1981, month=4, day=7))

        results = list(parse_repeating_interval('R11/PT1H2M/1980-03-05T01:01:00', relative=True))

        for dateindex in compat.range(0, 11):
             self.assertEqual(results[dateindex], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1) - dateindex * datetime.timedelta(hours=1, minutes=2))

        results = list(parse_repeating_interval('R2--1980-03-05T01:01:00--1981-04-05T01:01:00', intervaldelimiter='--', relative=True))
        self.assertEqual(results[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(results[1], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))

        results = list(parse_repeating_interval('R2/1980-03-05 01:01:00/1981-04-05 01:01:00', datetimedelimiter=' ', relative=True))
        self.assertEqual(results[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(results[1], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))

        #Make sure relative is correctly applied for months
        #https://bitbucket.org/nielsenb/aniso8601/issues/12/month-intervals-calculated-incorrectly-or
        results = list(parse_repeating_interval('R4/2017-04-30T00:00:00/P1M', relative=True))
        self.assertEqual(results[0], datetime.datetime(year=2017, month=4, day=30))
        self.assertEqual(results[1], datetime.datetime(year=2017, month=5, day=30))
        self.assertEqual(results[2], datetime.datetime(year=2017, month=6, day=30))
        self.assertEqual(results[3], datetime.datetime(year=2017, month=7, day=30))

        resultgenerator = parse_repeating_interval('R/PT1H2M/1980-03-05T01:01:00', relative=True)

        for dateindex in compat.range(0, 11):
             self.assertEqual(next(resultgenerator), datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1) - dateindex * datetime.timedelta(hours=1, minutes=2))

    def test_parse_repeating_interval_relative_suffixgarbage(self):
        #Don't allow garbage after the duration
        #https://bitbucket.org/nielsenb/aniso8601/issues/9/durations-with-trailing-garbage-are-parsed
        with self.assertRaises(ISOFormatError):
            parse_interval('R3/1981-04-05/P1Dasdf', relative=True)

        with self.assertRaises(ISOFormatError):
            parse_interval('R3/1981-04-05/P0003-06-04T12:30:05.5asdfasdf')
