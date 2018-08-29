# -*- coding: utf-8 -*-

# Copyright (c) 2018, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import mock
import unittest

from aniso8601.exceptions import ISOFormatError
from aniso8601.builder import TupleBuilder
from aniso8601.interval import _parse_interval, parse_interval, parse_repeating_interval

class TestIntervalParserFunctions(unittest.TestCase):
    def test_parse_interval(self):
        parse = parse_interval('P1M/1981-04-05T01:01:00', builder=TupleBuilder)
        self.assertEqual(parse, (None, (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (None, '1', None, None, None, None, None, 'duration'), 'interval'))

        parse = parse_interval('P1M/1981-04-05', builder=TupleBuilder)
        self.assertEqual(parse, (None, ('1981', '04', '05', None, None, None, 'date'), (None, '1', None, None, None, None, None, 'duration'), 'interval'))

        parse = parse_interval('P1.5Y/2018-03-06', builder=TupleBuilder)
        self.assertEqual(parse, (None, ('2018', '03', '06', None, None, None, 'date'), ('1.5', None, None, None, None, None, None, 'duration'), 'interval'))

        parse = parse_interval('PT1H/2014-11-12', builder=TupleBuilder)
        self.assertEqual(parse, (None, ('2014', '11', '12', None, None, None, 'date'), (None, None, None, None, '1', None, None, 'duration'), 'interval'))

        parse = parse_interval('PT4H54M6.5S/2014-11-12', builder=TupleBuilder)
        self.assertEqual(parse, (None, ('2014', '11', '12', None, None, None, 'date'), (None, None, None, None, '4', '54', '6.5', 'duration'), 'interval'))

        parse = parse_interval('PT0.0000001S/2018-03-06', builder=TupleBuilder)
        self.assertEqual(parse, (None, ('2018', '03', '06', None, None, None, 'date'), (None, None, None, None, None, None, '0.0000001', 'duration'), 'interval'))

        parse = parse_interval('PT2.0000048S/2018-03-06', builder=TupleBuilder)
        self.assertEqual(parse, (None, ('2018', '03', '06', None, None, None, 'date'), (None, None, None, None, None, None, '2.0000048', 'duration'), 'interval'))

        parse = parse_interval('1981-04-05T01:01:00/P1M1DT1M', builder=TupleBuilder)
        self.assertEqual(parse, ((('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, (None, '1', None, '1', None, '1', None, 'duration'), 'interval'))

        parse = parse_interval('1981-04-05/P1M1D', builder=TupleBuilder)
        self.assertEqual(parse, (('1981', '04', '05', None, None, None, 'date'), None, (None, '1', None, '1', None, None, None, 'duration'), 'interval'))

        parse = parse_interval('2018-03-06/P2.5M', builder=TupleBuilder)
        self.assertEqual(parse, (('2018', '03', '06', None, None, None, 'date'), None, (None, '2.5', None, None, None, None, None, 'duration'), 'interval'))

        parse = parse_interval('2014-11-12/PT1H', builder=TupleBuilder)
        self.assertEqual(parse, (('2014', '11', '12', None, None, None, 'date'), None, (None, None, None, None, '1', None, None, 'duration'), 'interval'))

        parse = parse_interval('2014-11-12/PT4H54M6.5S', builder=TupleBuilder)
        self.assertEqual(parse, (('2014', '11', '12', None, None, None, 'date'), None, (None, None, None, None, '4', '54', '6.5', 'duration'), 'interval'))

        parse = parse_interval('2018-03-06/PT0.0000001S', builder=TupleBuilder)
        self.assertEqual(parse, (('2018', '03', '06', None, None, None, 'date'), None, (None, None, None, None, None, None, '0.0000001', 'duration'), 'interval'))

        parse = parse_interval('2018-03-06/PT2.0000048S', builder=TupleBuilder)
        self.assertEqual(parse, (('2018', '03', '06', None, None, None, 'date'), None, (None, None, None, None, None, None, '2.0000048', 'duration'), 'interval'))

        parse = parse_interval('1980-03-05T01:01:00/1981-04-05T01:01:00', builder=TupleBuilder)
        self.assertEqual(parse, ((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, 'interval'))

        parse = parse_interval('1980-03-05T01:01:00/1981-04-05', builder=TupleBuilder)
        self.assertEqual(parse, ((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), ('1981', '04', '05', None, None, None, 'date'), None, 'interval'))

        parse = parse_interval('1980-03-05/1981-04-05T01:01:00', builder=TupleBuilder)
        self.assertEqual(parse, (('1980', '03', '05', None, None, None, 'date'), (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, 'interval'))

        parse = parse_interval('1980-03-05/1981-04-05', builder=TupleBuilder)
        self.assertEqual(parse, (('1980', '03', '05', None, None, None, 'date'), ('1981', '04', '05', None, None, None, 'date'), None, 'interval'))

        parse = parse_interval('1981-04-05/1980-03-05', builder=TupleBuilder)
        self.assertEqual(parse, (('1981', '04', '05', None, None, None, 'date'), ('1980', '03', '05', None, None, None, 'date'), None, 'interval'))

        parse = parse_interval('1980-03-05T01:01:00.0000001/1981-04-05T14:43:59.9999997', builder=TupleBuilder)
        self.assertEqual(parse, ((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00.0000001', None, 'time'), 'datetime'), (('1981', '04', '05', None, None, None, 'date'), ('14', '43', '59.9999997', None, 'time'), 'datetime'), None, 'interval'))

        #Test different separators
        parse = parse_interval('1980-03-05T01:01:00--1981-04-05T01:01:00', intervaldelimiter='--', builder=TupleBuilder)
        self.assertEqual(parse, ((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, 'interval'))

        parse = parse_interval('1980-03-05 01:01:00/1981-04-05 01:01:00', datetimedelimiter=' ', builder=TupleBuilder)
        self.assertEqual(parse, ((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, 'interval'))

    def test_parse_interval_defaultbuilder(self):
        import aniso8601

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('P1M/1981-04-05T01:01:00')

        mockBuildInterval.assert_called_once_with(end=(('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), duration=(None, '1', None, None, None, None, None, 'duration'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('P1M/1981-04-05')

        mockBuildInterval.assert_called_once_with(end=('1981', '04', '05', None, None, None, 'date'), duration=(None, '1', None, None, None, None, None, 'duration'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('P1.5Y/2018-03-06')

        mockBuildInterval.assert_called_once_with(end=('2018', '03', '06', None, None, None, 'date'), duration=('1.5', None, None, None, None, None, None, 'duration'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('PT1H/2014-11-12')

        mockBuildInterval.assert_called_once_with(end=('2014', '11', '12', None, None, None, 'date'), duration=(None, None, None, None, '1', None, None, 'duration'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('PT4H54M6.5S/2014-11-12')

        mockBuildInterval.assert_called_once_with(end=('2014', '11', '12', None, None, None, 'date'), duration=(None, None, None, None, '4', '54', '6.5', 'duration'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('PT0.0000001S/2018-03-06')

        mockBuildInterval.assert_called_once_with(end=('2018', '03', '06', None, None, None, 'date'), duration=(None, None, None, None, None, None, '0.0000001', 'duration'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('PT2.0000048S/2018-03-06')

        mockBuildInterval.assert_called_once_with(end=('2018', '03', '06', None, None, None, 'date'), duration=(None, None, None, None, None, None, '2.0000048', 'duration'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('1981-04-05T01:01:00/P1M1DT1M')

        mockBuildInterval.assert_called_once_with(start=(('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), duration=(None, '1', None, '1', None, '1', None, 'duration'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('1981-04-05/P1M1D')

        mockBuildInterval.assert_called_once_with(start=('1981', '04', '05', None, None, None, 'date'), duration=(None, '1', None, '1', None, None, None, 'duration'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('2018-03-06/P2.5M')

        mockBuildInterval.assert_called_once_with(start=('2018', '03', '06', None, None, None, 'date'), duration=(None, '2.5', None, None, None, None, None, 'duration'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('2014-11-12/PT1H')

        mockBuildInterval.assert_called_once_with(start=('2014', '11', '12', None, None, None, 'date'), duration=(None, None, None, None, '1', None, None, 'duration'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('2014-11-12/PT4H54M6.5S')

        mockBuildInterval.assert_called_once_with(start=('2014', '11', '12', None, None, None, 'date'), duration=(None, None, None, None, '4', '54', '6.5', 'duration'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('2018-03-06/PT0.0000001S')

        mockBuildInterval.assert_called_once_with(start=('2018', '03', '06', None, None, None, 'date'), duration=(None, None, None, None, None, None, '0.0000001', 'duration'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('2018-03-06/PT2.0000048S')

        mockBuildInterval.assert_called_once_with(start=('2018', '03', '06', None, None, None, 'date'), duration=(None, None, None, None, None, None, '2.0000048', 'duration'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('1980-03-05T01:01:00/1981-04-05T01:01:00')

        mockBuildInterval.assert_called_once_with(start=(('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), end=(('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('1980-03-05T01:01:00/1981-04-05')

        mockBuildInterval.assert_called_once_with(start=(('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), end=('1981', '04', '05', None, None, None, 'date'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('1980-03-05/1981-04-05T01:01:00')

        mockBuildInterval.assert_called_once_with(start=('1980', '03', '05', None, None, None, 'date'), end=(('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('1980-03-05/1981-04-05')

        mockBuildInterval.assert_called_once_with(start=('1980', '03', '05', None, None, None, 'date'), end=('1981', '04', '05', None, None, None, 'date'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('1981-04-05/1980-03-05')

        mockBuildInterval.assert_called_once_with(start=('1981', '04', '05', None, None, None, 'date'), end=('1980', '03', '05', None, None, None, 'date'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('1980-03-05T01:01:00.0000001/1981-04-05T14:43:59.9999997')

        mockBuildInterval.assert_called_once_with(start=(('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00.0000001', None, 'time'), 'datetime'), end=(('1981', '04', '05', None, None, None, 'date'), ('14', '43', '59.9999997', None, 'time'), 'datetime'))

        #Test different separators
        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('1980-03-05T01:01:00--1981-04-05T01:01:00', intervaldelimiter='--')

        mockBuildInterval.assert_called_once_with(start=(('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), end=(('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('1980-03-05 01:01:00/1981-04-05 01:01:00', datetimedelimiter=' ')

        mockBuildInterval.assert_called_once_with(start=(('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), end=(('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'))

    def test_parse_interval_mockbuilder(self):
        mockBuilder = mock.Mock()

        parse_interval('P1M/1981-04-05T01:01:00', builder=mockBuilder)

        mockBuilder.build_interval.assert_called_once_with(end=(('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), duration=(None, '1', None, None, None, None, None, 'duration'))

        mockBuilder = mock.Mock()

        parse_interval('2014-11-12/PT1H', builder=mockBuilder)

        mockBuilder.build_interval.assert_called_once_with(start=('2014', '11', '12', None, None, None, 'date'), duration=(None, None, None, None, '1', None, None, 'duration'))

        mockBuilder = mock.Mock()

        parse_interval('1980-03-05T01:01:00/1981-04-05T01:01:00', builder=mockBuilder)

        mockBuilder.build_interval.assert_called_once_with(start=(('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), end=(('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'))

    def test_parse_interval_relative(self):
        import aniso8601

        with mock.patch.object(aniso8601.builder.RelativeTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('P1M/1981-04-05T01:01:00', relative=True)

        mockBuildInterval.assert_called_once_with(end=(('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), duration=(None, '1', None, None, None, None, None, 'duration'))

        with mock.patch.object(aniso8601.builder.RelativeTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('2014-11-12/PT1H', relative=True)

        mockBuildInterval.assert_called_once_with(start=('2014', '11', '12', None, None, None, 'date'), duration=(None, None, None, None, '1', None, None, 'duration'))

        with mock.patch.object(aniso8601.builder.RelativeTimeBuilder, 'build_interval') as mockBuildInterval:
            parse_interval('1980-03-05T01:01:00/1981-04-05T01:01:00', relative=True)

        mockBuildInterval.assert_called_once_with(start=(('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), end=(('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'))

    def test_parse_interval_repeating(self):
        #Parse interval can't parse repeating intervals
        with self.assertRaises(ISOFormatError):
            parse_interval('R3/1981-04-05/P1D')

        with self.assertRaises(ISOFormatError):
            parse_interval('R3/1981-04-05/P0003-06-04T12:30:05.5')

        with self.assertRaises(ISOFormatError):
            parse_interval('R/PT1H2M/1980-03-05T01:01:00')

    def test_parse_interval_suffixgarbage(self):
        #Don't allow garbage after the duration
        #https://bitbucket.org/nielsenb/aniso8601/issues/9/durations-with-trailing-garbage-are-parsed
        with self.assertRaises(ValueError):
            parse_interval('2001/P1Dasdf', builder=TupleBuilder)

        with self.assertRaises(ValueError):
            parse_interval('P1Dasdf/2001', builder=TupleBuilder)

        with self.assertRaises(ValueError):
            parse_interval('2001/P0003-06-04T12:30:05.5asdfasdf', builder=TupleBuilder)

        with self.assertRaises(ValueError):
            parse_interval('P0003-06-04T12:30:05.5asdfasdf/2001', builder=TupleBuilder)

class TestRepeatingIntervalParserFunctions(unittest.TestCase):
    def test_parse_repeating_interval(self):
        parse = parse_repeating_interval('R3/1981-04-05/P1D', builder=TupleBuilder)
        self.assertEqual(parse, (False, '3', (('1981', '04', '05', None, None, None, 'date'), None, (None, None, None, '1', None, None, None, 'duration'), 'interval'), 'repeatinginterval'))

        parse = parse_repeating_interval('R11/PT1H2M/1980-03-05T01:01:00', builder=TupleBuilder)
        self.assertEqual(parse, (False, '11', (None, (('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (None, None, None, None, '1', '2', None, 'duration'), 'interval'), 'repeatinginterval'))

        parse = parse_repeating_interval('R2--1980-03-05T01:01:00--1981-04-05T01:01:00', intervaldelimiter='--', builder=TupleBuilder)
        self.assertEqual(parse, (False, '2', ((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, 'interval'), 'repeatinginterval'))

        parse = parse_repeating_interval('R2/1980-03-05 01:01:00/1981-04-05 01:01:00', datetimedelimiter=' ', builder=TupleBuilder)
        self.assertEqual(parse, (False, '2', ((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, 'interval'), 'repeatinginterval'))

        parse = parse_repeating_interval('R/PT1H2M/1980-03-05T01:01:00', builder=TupleBuilder)
        self.assertEqual(parse, (True, None, (None, (('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (None, None, None, None, '1', '2', None, 'duration'), 'interval'), 'repeatinginterval'))

    def test_parse_repeating_interval_defaultbuilder(self):
        import aniso8601

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_repeating_interval') as mockBuildRepeatingInterval:
            parse_repeating_interval('R3/1981-04-05/P1D')

        mockBuildRepeatingInterval.assert_called_once_with(R=False, Rnn='3', interval=(('1981', '04', '05', None, None, None, 'date'), None, (None, None, None, '1', None, None, None, 'duration'), 'interval'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_repeating_interval') as mockBuildRepeatingInterval:
            parse_repeating_interval('R11/PT1H2M/1980-03-05T01:01:00')

        mockBuildRepeatingInterval.assert_called_once_with(R=False, Rnn='11', interval=(None, (('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (None, None, None, None, '1', '2', None, 'duration'), 'interval'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_repeating_interval') as mockBuildRepeatingInterval:
            parse_repeating_interval('R2--1980-03-05T01:01:00--1981-04-05T01:01:00', intervaldelimiter='--')

        mockBuildRepeatingInterval.assert_called_once_with(R=False, Rnn='2', interval=((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, 'interval'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_repeating_interval') as mockBuildRepeatingInterval:
            parse_repeating_interval('R2/1980-03-05 01:01:00/1981-04-05 01:01:00', datetimedelimiter=' ')

        mockBuildRepeatingInterval.assert_called_once_with(R=False, Rnn='2', interval=((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, 'interval'))

        with mock.patch.object(aniso8601.builder.PythonTimeBuilder, 'build_repeating_interval') as mockBuildRepeatingInterval:
            parse_repeating_interval('R/PT1H2M/1980-03-05T01:01:00')

        mockBuildRepeatingInterval.assert_called_once_with(R=True, Rnn=None, interval=(None, (('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (None, None, None, None, '1', '2', None, 'duration'), 'interval'))

    def test_parse_repeating_interval_mockbuilder(self):
        mockBuilder = mock.Mock()

        parse_repeating_interval('R3/1981-04-05/P1D', builder=mockBuilder)

        mockBuilder.build_repeating_interval.assert_called_once_with(R=False, Rnn='3', interval=(('1981', '04', '05', None, None, None, 'date'), None, (None, None, None, '1', None, None, None, 'duration'), 'interval'))

        mockBuilder = mock.Mock()

        parse_repeating_interval('R11/PT1H2M/1980-03-05T01:01:00', builder=mockBuilder)

        mockBuilder.build_repeating_interval.assert_called_once_with(R=False, Rnn='11', interval=(None, (('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (None, None, None, None, '1', '2', None, 'duration'), 'interval'))

        mockBuilder = mock.Mock()

        parse_repeating_interval('R/PT1H2M/1980-03-05T01:01:00', builder=mockBuilder)

        mockBuilder.build_repeating_interval.assert_called_once_with(R=True, Rnn=None, interval=(None, (('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (None, None, None, None, '1', '2', None, 'duration'), 'interval'))

    def test_parse_repeating_interval_relative(self):
        import aniso8601

        with mock.patch.object(aniso8601.builder.RelativeTimeBuilder, 'build_repeating_interval') as mockBuildInterval:
            parse_repeating_interval('R3/1981-04-05/P1D', relative=True)

        mockBuildInterval.assert_called_once_with(R=False, Rnn='3', interval=(('1981', '04', '05', None, None, None, 'date'), None, (None, None, None, '1', None, None, None, 'duration'), 'interval'))

        with mock.patch.object(aniso8601.builder.RelativeTimeBuilder, 'build_repeating_interval') as mockBuildInterval:
            parse_repeating_interval('R11/PT1H2M/1980-03-05T01:01:00', relative=True)

        mockBuildInterval.assert_called_once_with(R=False, Rnn='11', interval=(None, (('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (None, None, None, None, '1', '2', None, 'duration'), 'interval'))

        with mock.patch.object(aniso8601.builder.RelativeTimeBuilder, 'build_repeating_interval') as mockBuildInterval:
            parse_repeating_interval('R/PT1H2M/1980-03-05T01:01:00', relative=True)

        mockBuildInterval.assert_called_once_with(R=True, Rnn=None, interval=(None, (('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (None, None, None, None, '1', '2', None, 'duration'), 'interval'))

    def test_parse_repeating_interval_suffixgarbage(self):
        #Don't allow garbage after the duration
        #https://bitbucket.org/nielsenb/aniso8601/issues/9/durations-with-trailing-garbage-are-parsed
        with self.assertRaises(ISOFormatError):
            parse_repeating_interval('R3/1981-04-05/P1Dasdf', builder=TupleBuilder)

        with self.assertRaises(ISOFormatError):
            parse_repeating_interval('R3/1981-04-05/P0003-06-04T12:30:05.5asdfasdf', builder=TupleBuilder)

    def test_parse_interval_internal(self):
        #Test the internal _parse_interval function
        parse = _parse_interval('P1M/1981-04-05T01:01:00', TupleBuilder)
        self.assertEqual(parse, (None, (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (None, '1', None, None, None, None, None, 'duration'), 'interval'))

        parse = _parse_interval('P1M/1981-04-05', TupleBuilder)
        self.assertEqual(parse, (None, ('1981', '04', '05', None, None, None, 'date'), (None, '1', None, None, None, None, None, 'duration'), 'interval'))

        parse = _parse_interval('P1.5Y/2018-03-06', TupleBuilder)
        self.assertEqual(parse, (None, ('2018', '03', '06', None, None, None, 'date'), ('1.5', None, None, None, None, None, None, 'duration'), 'interval'))

        parse = _parse_interval('PT1H/2014-11-12', TupleBuilder)
        self.assertEqual(parse, (None, ('2014', '11', '12', None, None, None, 'date'), (None, None, None, None, '1', None, None, 'duration'), 'interval'))

        parse = _parse_interval('PT4H54M6.5S/2014-11-12', TupleBuilder)
        self.assertEqual(parse, (None, ('2014', '11', '12', None, None, None, 'date'), (None, None, None, None, '4', '54', '6.5', 'duration'), 'interval'))

        parse = _parse_interval('PT0.0000001S/2018-03-06', TupleBuilder)
        self.assertEqual(parse, (None, ('2018', '03', '06', None, None, None, 'date'), (None, None, None, None, None, None, '0.0000001', 'duration'), 'interval'))

        parse = _parse_interval('PT2.0000048S/2018-03-06', TupleBuilder)
        self.assertEqual(parse, (None, ('2018', '03', '06', None, None, None, 'date'), (None, None, None, None, None, None, '2.0000048', 'duration'), 'interval'))

        parse = _parse_interval('1981-04-05T01:01:00/P1M1DT1M', TupleBuilder)
        self.assertEqual(parse, ((('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, (None, '1', None, '1', None, '1', None, 'duration'), 'interval'))

        parse = _parse_interval('1981-04-05/P1M1D', TupleBuilder)
        self.assertEqual(parse, (('1981', '04', '05', None, None, None, 'date'), None, (None, '1', None, '1', None, None, None, 'duration'), 'interval'))

        parse = _parse_interval('2018-03-06/P2.5M', TupleBuilder)
        self.assertEqual(parse, (('2018', '03', '06', None, None, None, 'date'), None, (None, '2.5', None, None, None, None, None, 'duration'), 'interval'))

        parse = _parse_interval('2014-11-12/PT1H', TupleBuilder)
        self.assertEqual(parse, (('2014', '11', '12', None, None, None, 'date'), None, (None, None, None, None, '1', None, None, 'duration'), 'interval'))

        parse = _parse_interval('2014-11-12/PT4H54M6.5S', TupleBuilder)
        self.assertEqual(parse, (('2014', '11', '12', None, None, None, 'date'), None, (None, None, None, None, '4', '54', '6.5', 'duration'), 'interval'))

        parse = _parse_interval('2018-03-06/PT0.0000001S', TupleBuilder)
        self.assertEqual(parse, (('2018', '03', '06', None, None, None, 'date'), None, (None, None, None, None, None, None, '0.0000001', 'duration'), 'interval'))

        parse = _parse_interval('2018-03-06/PT2.0000048S', TupleBuilder)
        self.assertEqual(parse, (('2018', '03', '06', None, None, None, 'date'), None, (None, None, None, None, None, None, '2.0000048', 'duration'), 'interval'))

        parse = _parse_interval('1980-03-05T01:01:00/1981-04-05T01:01:00', TupleBuilder)
        self.assertEqual(parse, ((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, 'interval'))

        parse = _parse_interval('1980-03-05T01:01:00/1981-04-05', TupleBuilder)
        self.assertEqual(parse, ((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), ('1981', '04', '05', None, None, None, 'date'), None, 'interval'))

        parse = _parse_interval('1980-03-05/1981-04-05T01:01:00', TupleBuilder)
        self.assertEqual(parse, (('1980', '03', '05', None, None, None, 'date'), (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, 'interval'))

        parse = _parse_interval('1980-03-05/1981-04-05', TupleBuilder)
        self.assertEqual(parse, (('1980', '03', '05', None, None, None, 'date'), ('1981', '04', '05', None, None, None, 'date'), None, 'interval'))

        parse = _parse_interval('1981-04-05/1980-03-05', TupleBuilder)
        self.assertEqual(parse, (('1981', '04', '05', None, None, None, 'date'), ('1980', '03', '05', None, None, None, 'date'), None, 'interval'))

        parse = _parse_interval('1980-03-05T01:01:00.0000001/1981-04-05T14:43:59.9999997', TupleBuilder)
        self.assertEqual(parse, ((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00.0000001', None, 'time'), 'datetime'), (('1981', '04', '05', None, None, None, 'date'), ('14', '43', '59.9999997', None, 'time'), 'datetime'), None, 'interval'))

        #Test different separators
        parse = _parse_interval('1980-03-05T01:01:00--1981-04-05T01:01:00', TupleBuilder, intervaldelimiter='--')
        self.assertEqual(parse, ((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, 'interval'))

        parse = _parse_interval('1980-03-05 01:01:00/1981-04-05 01:01:00', TupleBuilder, datetimedelimiter=' ')
        self.assertEqual(parse, ((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, 'interval'))
