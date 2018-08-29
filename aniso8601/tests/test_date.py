# -*- coding: utf-8 -*-

# Copyright (c) 2018, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import mock
import unittest

from aniso8601.builder import TupleBuilder
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
        parse = parse_date('2013', builder=TupleBuilder)
        self.assertEqual(parse, ('2013', None, None, None, None, None, 'date'))

        parse = parse_date('0001', builder=TupleBuilder)
        self.assertEqual(parse, ('0001', None, None, None, None, None, 'date'))

        parse = parse_date('19', builder=TupleBuilder)
        self.assertEqual(parse, ('19', None, None, None, None, None, 'date'))

        parse = parse_date('1981-04-05', builder=TupleBuilder)
        self.assertEqual(parse, ('1981', '04', '05', None, None, None, 'date'))

        parse = parse_date('19810405', builder=TupleBuilder)
        self.assertEqual(parse, ('1981', '04', '05', None, None, None, 'date'))

        parse = parse_date('1981-04', builder=TupleBuilder)
        self.assertEqual(parse, ('1981', '04', None, None, None, None, 'date'))

        parse = parse_date('2004-W53', builder=TupleBuilder)
        self.assertEqual(parse, ('2004', None, None, '53', None, None, 'date'))

        parse = parse_date('2009-W01', builder=TupleBuilder)
        self.assertEqual(parse, ('2009', None, None, '01', None, None, 'date'))

        parse = parse_date('2004-W53-6', builder=TupleBuilder)
        self.assertEqual(parse, ('2004', None, None, '53', '6', None, 'date'))

        parse = parse_date('2004W53', builder=TupleBuilder)
        self.assertEqual(parse, ('2004', None, None, '53', None, None, 'date'))

        parse = parse_date('2004W536', builder=TupleBuilder)
        self.assertEqual(parse, ('2004', None, None, '53', '6', None, 'date'))

        parse = parse_date('1981-095', builder=TupleBuilder)
        self.assertEqual(parse, ('1981', None, None, None, None, '095', 'date'))

        parse = parse_date('1981095', builder=TupleBuilder)
        self.assertEqual(parse, ('1981', None, None, None, None, '095', 'date'))

    def test_parse_date_defaultbuilder(self):
        import aniso8601

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_date') as mockBuildDate:
            parse_date('2013')

        mockBuildDate.assert_called_once_with(YYYY='2013')

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_date') as mockBuildDate:
            parse_date('0001')

        mockBuildDate.assert_called_once_with(YYYY='0001')

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_date') as mockBuildDate:
            parse_date('19')

        mockBuildDate.assert_called_once_with(YYYY='19')

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_date') as mockBuildDate:
            parse_date('1981-04-05')

        mockBuildDate.assert_called_once_with(YYYY='1981', MM='04', DD='05')

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_date') as mockBuildDate:
            parse_date('19810405')

        mockBuildDate.assert_called_once_with(YYYY='1981', MM='04', DD='05')

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_date') as mockBuildDate:
            parse_date('1981-04')

        mockBuildDate.assert_called_once_with(YYYY='1981', MM='04')

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_date') as mockBuildDate:
            parse_date('2004-W53')

        mockBuildDate.assert_called_once_with(YYYY='2004', Www='53')

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_date') as mockBuildDate:
            parse_date('2009-W01')

        mockBuildDate.assert_called_once_with(YYYY='2009', Www='01')

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_date') as mockBuildDate:
            parse_date('2004-W53-6')

        mockBuildDate.assert_called_once_with(YYYY='2004', Www='53', D='6')

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_date') as mockBuildDate:
            parse_date('2004W53')

        mockBuildDate.assert_called_once_with(YYYY='2004', Www='53')

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_date') as mockBuildDate:
            parse_date('2004W536')

        mockBuildDate.assert_called_once_with(YYYY='2004', Www='53', D='6')

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_date') as mockBuildDate:
            parse_date('1981-095')

        mockBuildDate.assert_called_once_with(YYYY='1981', DDD='095')

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_date') as mockBuildDate:
            parse_date('1981095')

        mockBuildDate.assert_called_once_with(YYYY='1981', DDD='095')

    def test_parse_year(self):
        parse = _parse_year('2013', TupleBuilder)
        self.assertEqual(parse, ('2013', None, None, None, None, None, 'date'))

        parse = _parse_year('0001', TupleBuilder)
        self.assertEqual(parse, ('0001', None, None, None, None, None, 'date'))

        parse = _parse_year('19', TupleBuilder)
        self.assertEqual(parse, ('19', None, None, None, None, None, 'date'))

    def test_parse_calendar_day(self):
        parse = _parse_calendar_day('1981-04-05', TupleBuilder)
        self.assertEqual(parse, ('1981', '04', '05', None, None, None, 'date'))

        parse = _parse_calendar_day('19810405', TupleBuilder)
        self.assertEqual(parse, ('1981', '04', '05', None, None, None, 'date'))

    def test_parse_calendar_month(self):
        parse = _parse_calendar_month('1981-04', TupleBuilder)
        self.assertEqual(parse, ('1981', '04', None, None, None, None, 'date'))

    def test_parse_calendar_month_nohyphen(self):
        #Hyphen is required
        with self.assertRaises(ISOFormatError):
            _parse_calendar_month('198104', None)

    def test_parse_week_day(self):
        parse = _parse_week_day('2004-W53-6', TupleBuilder)
        self.assertEqual(parse, ('2004', None, None, '53', '6', None, 'date'))

        parse = _parse_week_day('2009-W01-1', TupleBuilder)
        self.assertEqual(parse, ('2009', None, None, '01', '1', None, 'date'))

        parse = _parse_week_day('2009-W53-7', TupleBuilder)
        self.assertEqual(parse, ('2009', None, None, '53', '7', None, 'date'))

        parse = _parse_week_day('2010-W01-1', TupleBuilder)
        self.assertEqual(parse, ('2010', None, None, '01', '1', None, 'date'))

        parse = _parse_week_day('2004W536', TupleBuilder)
        self.assertEqual(parse, ('2004', None, None, '53', '6', None, 'date'))

        parse = _parse_week_day('2009W011', TupleBuilder)
        self.assertEqual(parse, ('2009', None, None, '01', '1', None, 'date'))

        parse = _parse_week_day('2009W537', TupleBuilder)
        self.assertEqual(parse, ('2009', None, None, '53', '7', None, 'date'))

        parse = _parse_week_day('2010W011', TupleBuilder)
        self.assertEqual(parse, ('2010', None, None, '01', '1', None, 'date'))

    def test_parse_week(self):
        parse = _parse_week('2004-W53', TupleBuilder)
        self.assertEqual(parse, ('2004', None, None, '53', None, None, 'date'))

        parse = _parse_week('2009-W01', TupleBuilder)
        self.assertEqual(parse, ('2009', None, None, '01', None, None, 'date'))

        parse = _parse_week('2009-W53', TupleBuilder)
        self.assertEqual(parse, ('2009', None, None, '53', None, None, 'date'))

        parse = _parse_week('2010-W01', TupleBuilder)
        self.assertEqual(parse, ('2010', None, None, '01', None, None, 'date'))

        parse = _parse_week('2004W53', TupleBuilder)
        self.assertEqual(parse, ('2004', None, None, '53', None, None, 'date'))

        parse = _parse_week('2009W01', TupleBuilder)
        self.assertEqual(parse, ('2009', None, None, '01', None, None, 'date'))

        parse = _parse_week('2009W53', TupleBuilder)
        self.assertEqual(parse, ('2009', None, None, '53', None, None, 'date'))

        parse = _parse_week('2010W01', TupleBuilder)
        self.assertEqual(parse, ('2010', None, None, '01', None, None, 'date'))

    def test_parse_ordinal_date(self):
        parse = _parse_ordinal_date('1981-095', TupleBuilder)
        self.assertEqual(parse, ('1981', None, None, None, None, '095', 'date'))

        parse = _parse_ordinal_date('1981095', TupleBuilder)
        self.assertEqual(parse, ('1981', None, None, None, None, '095', 'date'))

        parse = _parse_ordinal_date('1981365', TupleBuilder)
        self.assertEqual(parse, ('1981', None, None, None, None, '365', 'date'))

        parse = _parse_ordinal_date('1980366', TupleBuilder)
        self.assertEqual(parse, ('1980', None, None, None, None, '366', 'date'))
