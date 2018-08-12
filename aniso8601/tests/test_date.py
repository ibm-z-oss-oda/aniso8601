# -*- coding: utf-8 -*-

# Copyright (c) 2018, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import unittest

from aniso8601.builder import NoneBuilder
from aniso8601.exceptions import ISOFormatError
from aniso8601.date import parse_date, _parse_year, _parse_calendar_day, \
        _parse_calendar_month, _parse_week_day, _parse_week, \
        _parse_ordinal_date, get_date_resolution
from aniso8601.resolution import DateResolution

class TestDateResolutionFunctions(unittest.TestCase):
    def test_get_date_resolution_year(self):
        self.assertEqual(get_date_resolution('2013'), DateResolution.Year)
        self.assertEqual(get_date_resolution('0001'), DateResolution.Year)
        self.assertEqual(get_date_resolution('19'), DateResolution.Year)

    def test_get_date_resolution_month(self):
        self.assertEqual(get_date_resolution('1981-04'), DateResolution.Month)

    def test_get_date_resolution_week(self):
        self.assertEqual(get_date_resolution('2004-W53'), DateResolution.Week)
        self.assertEqual(get_date_resolution('2009-W01'), DateResolution.Week)
        self.assertEqual(get_date_resolution('2004W53'), DateResolution.Week)

    def test_get_date_resolution_year_weekday(self):
        self.assertEqual(get_date_resolution('2004-W53-6'), DateResolution.Weekday)
        self.assertEqual(get_date_resolution('2004W536'), DateResolution.Weekday)

    def test_get_date_resolution_year_ordinal(self):
        self.assertEqual(get_date_resolution('1981-095'), DateResolution.Ordinal)
        self.assertEqual(get_date_resolution('1981095'), DateResolution.Ordinal)

class TestDateParserFunctions(unittest.TestCase):
    def test_parse_date(self):
        parse = parse_date('2013', builder=NoneBuilder)
        self.assertEqual(parse, ('2013', None, None, None, None, None))

        parse = parse_date('0001', builder=NoneBuilder)
        self.assertEqual(parse, ('0001', None, None, None, None, None))

        parse = parse_date('19', builder=NoneBuilder)
        self.assertEqual(parse, ('1900', None, None, None, None, None))

        parse = parse_date('1981-04-05', builder=NoneBuilder)
        self.assertEqual(parse, ('1981', '04', '05', None, None, None))

        parse = parse_date('19810405', builder=NoneBuilder)
        self.assertEqual(parse, ('1981', '04', '05', None, None, None))

        parse = parse_date('1981-04', builder=NoneBuilder)
        self.assertEqual(parse, ('1981', '04', None, None, None, None))

        parse = parse_date('2004-W53', builder=NoneBuilder)
        self.assertEqual(parse, ('2004', None, None, '53', None, None))

        parse = parse_date('2009-W01', builder=NoneBuilder)
        self.assertEqual(parse, ('2009', None, None, '01', None, None))

        parse = parse_date('2004-W53-6', builder=NoneBuilder)
        self.assertEqual(parse, ('2004', None, None, '53', '6', None))

        parse = parse_date('2004W53', builder=NoneBuilder)
        self.assertEqual(parse, ('2004', None, None, '53', None, None))

        parse = parse_date('2004W536', builder=NoneBuilder)
        self.assertEqual(parse, ('2004', None, None, '53', '6', None))

        parse = parse_date('1981-095', builder=NoneBuilder)
        self.assertEqual(parse, ('1981', None, None, None, None, '095'))

        parse = parse_date('1981095', builder=NoneBuilder)
        self.assertEqual(parse, ('1981', None, None, None, None, '095'))

    def test_parse_year(self):
        parse = _parse_year('2013', NoneBuilder)
        self.assertEqual(parse, ('2013', None, None, None, None, None))

        parse = _parse_year('0001', NoneBuilder)
        self.assertEqual(parse, ('0001', None, None, None, None, None))

        parse = _parse_year('19', NoneBuilder)
        self.assertEqual(parse, ('1900', None, None, None, None, None))

    def test_parse_calendar_day(self):
        parse = _parse_calendar_day('1981-04-05', NoneBuilder)
        self.assertEqual(parse, ('1981', '04', '05', None, None, None))

        parse = _parse_calendar_day('19810405', NoneBuilder)
        self.assertEqual(parse, ('1981', '04', '05', None, None, None))

    def test_parse_calendar_month(self):
        parse = _parse_calendar_month('1981-04', NoneBuilder)
        self.assertEqual(parse, ('1981', '04', None, None, None, None))

    def test_parse_calendar_month_nohyphen(self):
        #Hyphen is required
        with self.assertRaises(ISOFormatError):
            _parse_calendar_month('198104', NoneBuilder)

    def test_parse_week_day(self):
        parse = _parse_week_day('2004-W53-6', NoneBuilder)
        self.assertEqual(parse, ('2004', None, None, '53', '6', None))

        parse = _parse_week_day('2009-W01-1', NoneBuilder)
        self.assertEqual(parse, ('2009', None, None, '01', '1', None))

        parse = _parse_week_day('2009-W53-7', NoneBuilder)
        self.assertEqual(parse, ('2009', None, None, '53', '7', None))

        parse = _parse_week_day('2010-W01-1', NoneBuilder)
        self.assertEqual(parse, ('2010', None, None, '01', '1', None))

        parse = _parse_week_day('2004W536', NoneBuilder)
        self.assertEqual(parse, ('2004', None, None, '53', '6', None))

        parse = _parse_week_day('2009W011', NoneBuilder)
        self.assertEqual(parse, ('2009', None, None, '01', '1', None))

        parse = _parse_week_day('2009W537', NoneBuilder)
        self.assertEqual(parse, ('2009', None, None, '53', '7', None))

        parse = _parse_week_day('2010W011', NoneBuilder)
        self.assertEqual(parse, ('2010', None, None, '01', '1', None))

    def test_parse_week(self):
        parse = _parse_week('2004-W53', NoneBuilder)
        self.assertEqual(parse, ('2004', None, None, '53', None, None))

        parse = _parse_week('2009-W01', NoneBuilder)
        self.assertEqual(parse, ('2009', None, None, '01', None, None))

        parse = _parse_week('2009-W53', NoneBuilder)
        self.assertEqual(parse, ('2009', None, None, '53', None, None))

        parse = _parse_week('2010-W01', NoneBuilder)
        self.assertEqual(parse, ('2010', None, None, '01', None, None))

        parse = _parse_week('2004W53', NoneBuilder)
        self.assertEqual(parse, ('2004', None, None, '53', None, None))

        parse = _parse_week('2009W01', NoneBuilder)
        self.assertEqual(parse, ('2009', None, None, '01', None, None))

        parse = _parse_week('2009W53', NoneBuilder)
        self.assertEqual(parse, ('2009', None, None, '53', None, None))

        parse = _parse_week('2010W01', NoneBuilder)
        self.assertEqual(parse, ('2010', None, None, '01', None, None))

    def test_parse_ordinal_date(self):
        parse = _parse_ordinal_date('1981-095', NoneBuilder)
        self.assertEqual(parse, ('1981', None, None, None, None, '095'))

        parse = _parse_ordinal_date('1981095', NoneBuilder)
        self.assertEqual(parse, ('1981', None, None, None, None, '095'))

        parse = _parse_ordinal_date('1981365', NoneBuilder)
        self.assertEqual(parse, ('1981', None, None, None, None, '365'))

        parse = _parse_ordinal_date('1980366', NoneBuilder)
        self.assertEqual(parse, ('1980', None, None, None, None, '366'))
