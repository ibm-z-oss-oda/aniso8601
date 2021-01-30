# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import unittest
import aniso8601

from aniso8601.builders import (DateTuple, DatetimeTuple,
                                DurationTuple, IntervalTuple, TimeTuple,
                                TimezoneTuple)
from aniso8601.exceptions import ISOFormatError
from aniso8601.interval import (_parse_interval, _parse_interval_end,
                                parse_interval, parse_repeating_interval)
from aniso8601.tests.compat import mock

class TestIntervalParserFunctions(unittest.TestCase):
    def test_parse_interval(self):
        testtuples = (('P1M/1981-04-05T01:01:00',
                       {'end': DatetimeTuple(DateTuple('1981', '04', '05',
                                                       None, None, None),
                                             TimeTuple('01', '01', '00',
                                                       None)),
                        'duration': DurationTuple(None, '1', None, None,
                                                  None, None, None)}),
                      ('P1M/1981-04-05',
                       {'end': DateTuple('1981', '04', '05', None, None, None),
                        'duration': DurationTuple(None, '1', None, None,
                                                  None, None, None)}),
                      ('P1,5Y/2018-03-06',
                       {'end': DateTuple('2018', '03', '06', None, None, None),
                        'duration': DurationTuple('1.5', None, None, None,
                                                  None, None, None)}),
                      ('P1.5Y/2018-03-06',
                       {'end': DateTuple('2018', '03', '06', None, None, None),
                        'duration': DurationTuple('1.5', None, None, None,
                                                  None, None, None)}),
                      ('PT1H/2014-11-12',
                       {'end': DateTuple('2014', '11', '12', None, None, None),
                        'duration': DurationTuple(None, None, None, None,
                                                  '1', None, None)}),
                      ('PT4H54M6.5S/2014-11-12',
                       {'end': DateTuple('2014', '11', '12', None, None, None),
                        'duration': DurationTuple(None, None, None, None,
                                                  '4', '54', '6.5')}),
                      ('PT10H/2050-03-01T13:00:00Z',
                       {'end': DatetimeTuple(DateTuple('2050', '03', '01',
                                                       None, None, None),
                                             TimeTuple('13', '00', '00',
                                                       TimezoneTuple(False,
                                                                     True,
                                                                     None,
                                                                     None,
                                                                     'Z'))),
                        'duration': DurationTuple(None, None, None,
                                                  None, '10', None, None)}),
                      #Make sure we truncate, not round
                      #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
                      ('PT0.0000001S/2018-03-06',
                       {'end': DateTuple('2018', '03', '06', None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '0.0000001')}),
                      ('PT2.0000048S/2018-03-06',
                       {'end': DateTuple('2018', '03', '06', None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '2.0000048')}),
                      ('1981-04-05T01:01:00/P1M1DT1M',
                       {'start': DatetimeTuple(DateTuple('1981', '04', '05',
                                                         None, None, None),
                                               TimeTuple('01', '01',
                                                         '00', None)),
                        'duration': DurationTuple(None, '1', None,
                                                  '1', None, '1', None)}),
                      ('1981-04-05/P1M1D',
                       {'start': DateTuple('1981', '04', '05',
                                           None, None, None),
                        'duration': DurationTuple(None, '1', None,
                                                  '1', None, None, None)}),
                      ('2018-03-06/P2,5M',
                       {'start': DateTuple('2018', '03', '06',
                                           None, None, None),
                        'duration': DurationTuple(None, '2.5', None,
                                                  None, None, None, None)}),
                      ('2018-03-06/P2.5M',
                       {'start': DateTuple('2018', '03', '06',
                                           None, None, None),
                        'duration': DurationTuple(None, '2.5', None,
                                                  None, None, None, None)}),
                      ('2014-11-12/PT1H',
                       {'start': DateTuple('2014', '11', '12',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, '1', None, None)}),
                      ('2014-11-12/PT4H54M6.5S',
                       {'start': DateTuple('2014', '11', '12',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, '4', '54', '6.5')}),
                      ('2050-03-01T13:00:00Z/PT10H',
                       {'start': DatetimeTuple(DateTuple('2050', '03', '01',
                                                         None, None, None),
                                               TimeTuple('13', '00', '00',
                                                         TimezoneTuple(False,
                                                                       True,
                                                                       None,
                                                                       None,
                                                                       'Z'))),
                        'duration': DurationTuple(None, None, None,
                                                  None, '10', None, None)}),
                      #Make sure we truncate, not round
                      #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
                      ('2018-03-06/PT0.0000001S',
                       {'start': DateTuple('2018', '03', '06',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '0.0000001')}),
                      ('2018-03-06/PT2.0000048S',
                       {'start': DateTuple('2018', '03', '06',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '2.0000048')}),
                      ('1980-03-05T01:01:00/1981-04-05T01:01:00',
                       {'start': DatetimeTuple(DateTuple('1980', '03', '05',
                                                         None, None, None),
                                               TimeTuple('01', '01', '00',
                                                         None)),
                        'end': DatetimeTuple(DateTuple('1981', '04', '05',
                                                       None, None, None),
                                             TimeTuple('01', '01', '00',
                                                       None))}),
                      ('1980-03-05T01:01:00/1981-04-05',
                       {'start': DatetimeTuple(DateTuple('1980', '03', '05',
                                                         None, None, None),
                                  TimeTuple('01', '01', '00',
                                            None)),
                        'end': DateTuple('1981', '04', '05',
                                         None, None, None)}),
                      ('1980-03-05/1981-04-05T01:01:00',
                       {'start': DateTuple('1980', '03', '05',
                                           None, None, None),
                        'end': DatetimeTuple(DateTuple('1981', '04', '05',
                                                       None, None, None),
                                             TimeTuple('01', '01', '00',
                                                       None))}),
                      ('1980-03-05/1981-04-05',
                       {'start': DateTuple('1980', '03', '05',
                                           None, None, None),
                        'end': DateTuple('1981', '04', '05',
                                         None, None, None)}),
                      ('1981-04-05/1980-03-05',
                       {'start': DateTuple('1981', '04', '05',
                                           None, None, None),
                        'end': DateTuple('1980', '03', '05',
                                         None, None, None)}),
                      ('2050-03-01T13:00:00Z/2050-05-11T15:30:00Z',
                       {'start': DatetimeTuple(DateTuple('2050', '03', '01',
                                                         None, None, None),
                                               TimeTuple('13', '00', '00',
                                               TimezoneTuple(False, True,
                                                             None, None,
                                                             'Z'))),
                        'end': DatetimeTuple(DateTuple('2050', '05', '11',
                                                       None, None, None),
                                             TimeTuple('15', '30', '00',
                                             TimezoneTuple(False, True,
                                                           None, None,
                                                           'Z')))}),
                      #Test concise interval
                      ('2020-01-01/02',
                       {'start': DateTuple('2020', '01', '01',
                                           None, None, None),
                        'end': DateTuple(None, None, '02',
                                         None, None, None)}),
                      ('2008-02-15/03-14',
                       {'start': DateTuple('2008', '02', '15',
                                           None, None, None),
                        'end': DateTuple(None, '03', '14',
                                         None, None, None)}),
                      ('2007-12-14T13:30/15:30',
                       {'start': DatetimeTuple(DateTuple('2007', '12', '14',
                                                         None, None, None),
                                               TimeTuple('13', '30', None,
                                                         None)),
                        'end': TimeTuple('15', '30', None,
                                         None)}),
                      ('2007-11-13T09:00/15T17:00',
                       {'start': DatetimeTuple(DateTuple('2007', '11', '13',
                                                         None, None, None),
                                               TimeTuple('09', '00', None,
                                                         None)),
                        'end': DatetimeTuple(DateTuple(None, None, '15',
                                                       None, None, None),
                                             TimeTuple('17', '00', None,
                                                       None))}),
                      ('2007-11-13T00:00/16T00:00',
                       {'start': DatetimeTuple(DateTuple('2007', '11', '13',
                                                         None, None, None),
                                               TimeTuple('00', '00', None,
                                                         None)),
                        'end': DatetimeTuple(DateTuple(None, None, '16',
                                                       None, None, None),
                                             TimeTuple('00', '00', None,
                                                       None))}),
                      ('2007-11-13T09:00Z/15T17:00',
                       {'start': DatetimeTuple(DateTuple('2007', '11', '13',
                                                         None, None, None),
                                               TimeTuple('09', '00', None,
                                                         TimezoneTuple(False,
                                                                       True,
                                                                       None,
                                                                       None,
                                                                       'Z'))),
                        'end': DatetimeTuple(DateTuple(None, None, '15',
                                                       None, None, None),
                                             TimeTuple('17', '00', None,
                                                       None))}),
                      ('2007-11-13T00:00/12:34.567',
                       {'start': DatetimeTuple(DateTuple('2007', '11', '13',
                                                         None, None, None),
                                               TimeTuple('00', '00', None,
                                                         None)),
                        'end': TimeTuple('12', '34.567', None,
                                         None)}),
                      #Make sure we truncate, not round
                      #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
                      ('1980-03-05T01:01:00.0000001/'
                       '1981-04-05T14:43:59.9999997',
                       {'start': DatetimeTuple(DateTuple('1980', '03', '05',
                                                         None, None, None),
                                               TimeTuple('01', '01',
                                                         '00.0000001',
                                                         None)),
                        'end': DatetimeTuple(DateTuple('1981', '04', '05',
                                                       None, None, None),
                                             TimeTuple('14', '43',
                                                       '59.9999997', None))}))

        for testtuple in testtuples:
            with mock.patch.object(aniso8601.interval.PythonTimeBuilder,
                                   'build_interval') as mockBuildInterval:
                mockBuildInterval.return_value = testtuple[1]

                result = parse_interval(testtuple[0])

                self.assertEqual(result, testtuple[1])
                mockBuildInterval.assert_called_once_with(**testtuple[1])

        #Test different separators
        with mock.patch.object(aniso8601.interval.PythonTimeBuilder,
                               'build_interval') as mockBuildInterval:
            expectedargs = {'start': DatetimeTuple(DateTuple('1980', '03',
                                                             '05', None,
                                                             None, None),
                                                   TimeTuple('01', '01',
                                                             '00', None)),
                            'end': DatetimeTuple(DateTuple('1981', '04',
                                                           '05', None,
                                                           None, None),
                                                 TimeTuple('01', '01',
                                                           '00', None))}

            mockBuildInterval.return_value = expectedargs

            result = parse_interval('1980-03-05T01:01:00--1981-04-05T01:01:00',
                                    intervaldelimiter='--')

            self.assertEqual(result, expectedargs)
            mockBuildInterval.assert_called_once_with(**expectedargs)

        with mock.patch.object(aniso8601.interval.PythonTimeBuilder,
                               'build_interval') as mockBuildInterval:
            expectedargs = {'start': DatetimeTuple(DateTuple('1980', '03',
                                                             '05', None,
                                                             None, None),
                                      TimeTuple('01', '01', '00', None)),
                            'end': DatetimeTuple(DateTuple('1981', '04',
                                                           '05', None,
                                                           None, None),
                                                 TimeTuple('01', '01',
                                                           '00', None))}

            mockBuildInterval.return_value = expectedargs

            result = parse_interval('1980-03-05 01:01:00/1981-04-05 01:01:00',
                                    datetimedelimiter=' ')

            self.assertEqual(result, expectedargs)
            mockBuildInterval.assert_called_once_with(**expectedargs)

    def test_parse_interval_mockbuilder(self):
        mockBuilder = mock.Mock()

        expectedargs = {'end': DatetimeTuple(DateTuple('1981', '04', '05',
                                                       None, None, None),
                                             TimeTuple('01', '01', '00',
                                                       None)),
                        'duration': DurationTuple(None, '1', None, None,
                                                  None, None, None)}

        mockBuilder.build_interval.return_value = expectedargs

        result = parse_interval('P1M/1981-04-05T01:01:00', builder=mockBuilder)

        self.assertEqual(result, expectedargs)
        mockBuilder.build_interval.assert_called_once_with(**expectedargs)

        mockBuilder = mock.Mock()

        expectedargs = {'start': DateTuple('2014', '11', '12',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None, None,
                                                  '1', None, None)}

        mockBuilder.build_interval.return_value = expectedargs

        result = parse_interval('2014-11-12/PT1H', builder=mockBuilder)

        self.assertEqual(result, expectedargs)
        mockBuilder.build_interval.assert_called_once_with(**expectedargs)

        mockBuilder = mock.Mock()

        expectedargs = {'start': DatetimeTuple(DateTuple('1980', '03', '05',
                                                         None, None, None),
                                               TimeTuple('01', '01', '00',
                                                         None)),
                        'end': DatetimeTuple(DateTuple('1981', '04', '05',
                                                       None, None, None),
                                             TimeTuple('01', '01', '00',
                                                       None))}

        mockBuilder.build_interval.return_value = expectedargs

        result = parse_interval('1980-03-05T01:01:00/1981-04-05T01:01:00',
                       builder=mockBuilder)

        self.assertEqual(result, expectedargs)
        mockBuilder.build_interval.assert_called_once_with(**expectedargs)

    def test_parse_interval_badtype(self):
        testtuples = (None, 1, False, 1.234)

        for testtuple in testtuples:
            with self.assertRaises(ValueError):
                parse_interval(testtuple, builder=None)

    def test_parse_interval_baddelimiter(self):
        testtuples = ('1980-03-05T01:01:00,1981-04-05T01:01:00',
                      'P1M 1981-04-05T01:01:00')

        for testtuple in testtuples:
            with self.assertRaises(ISOFormatError):
                parse_interval(testtuple, builder=None)

    def test_parse_interval_badstr(self):
        testtuples = ('/', '0/0/0', '20.50230/0', '5/%', '1/21', 'bad', '')

        for testtuple in testtuples:
            with self.assertRaises(ISOFormatError):
                parse_interval(testtuple, builder=None)

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
        with self.assertRaises(ISOFormatError):
            parse_interval('2001/P1Dasdf', builder=None)

        with self.assertRaises(ISOFormatError):
            parse_interval('P1Dasdf/2001', builder=None)

        with self.assertRaises(ISOFormatError):
            parse_interval('2001/P0003-06-04T12:30:05.5asdfasdf', builder=None)

        with self.assertRaises(ISOFormatError):
            parse_interval('P0003-06-04T12:30:05.5asdfasdf/2001', builder=None)

    def test_parse_interval_internal(self):
        #Test the internal _parse_interval function
        testtuples = (('P1M/1981-04-05T01:01:00',
                       {'end': DatetimeTuple(DateTuple('1981', '04', '05',
                                                       None, None, None),
                                             TimeTuple('01', '01', '00', None)),
                        'duration': DurationTuple(None, '1', None, None,
                                                  None, None, None)}),
                      ('P1M/1981-04-05',
                       {'end': DateTuple('1981', '04', '05', None, None, None),
                        'duration': DurationTuple(None, '1', None, None,
                                                  None, None, None)}),
                      ('P1,5Y/2018-03-06',
                       {'end': DateTuple('2018', '03', '06', None, None, None),
                        'duration': DurationTuple('1.5', None, None, None,
                                                  None, None, None)}),
                      ('P1.5Y/2018-03-06',
                       {'end': DateTuple('2018', '03', '06', None, None, None),
                        'duration': DurationTuple('1.5', None, None, None,
                                                  None, None, None)}),
                      ('PT1H/2014-11-12',
                       {'end': DateTuple('2014', '11', '12', None, None, None),
                        'duration': DurationTuple(None, None, None, None,
                                                  '1', None, None)}),
                      ('PT4H54M6.5S/2014-11-12',
                       {'end': DateTuple('2014', '11', '12', None, None, None),
                        'duration': DurationTuple(None, None, None, None,
                                                  '4', '54', '6.5')}),
                      #Make sure we truncate, not round
                      #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
                      ('PT0.0000001S/2018-03-06',
                       {'end': DateTuple('2018', '03', '06', None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '0.0000001')}),
                      ('PT2.0000048S/2018-03-06',
                       {'end': DateTuple('2018', '03', '06', None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '2.0000048')}),
                      ('1981-04-05T01:01:00/P1M1DT1M',
                       {'start': DatetimeTuple(DateTuple('1981', '04', '05',
                                                         None, None, None),
                                               TimeTuple('01', '01', '00', None)),
                        'duration': DurationTuple(None, '1', None,
                                                  '1', None, '1', None)}),
                      ('1981-04-05/P1M1D',
                       {'start': DateTuple('1981', '04', '05',
                                           None, None, None),
                        'duration': DurationTuple(None, '1', None,
                                                  '1', None, None, None)}),
                      ('2018-03-06/P2,5M',
                       {'start': DateTuple('2018', '03', '06',
                                           None, None, None),
                        'duration': DurationTuple(None, '2.5', None,
                                                  None, None, None, None)}),
                      ('2018-03-06/P2.5M',
                       {'start': DateTuple('2018', '03', '06',
                                           None, None, None),
                        'duration': DurationTuple(None, '2.5', None,
                                                  None, None, None, None)}),
                      ('2014-11-12/PT1H',
                       {'start': DateTuple('2014', '11', '12',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, '1', None, None)}),
                      ('2014-11-12/PT4H54M6.5S',
                       {'start': DateTuple('2014', '11', '12',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, '4', '54', '6.5')}),
                      #Make sure we truncate, not round
                      #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
                      ('2018-03-06/PT0.0000001S',
                       {'start': DateTuple('2018', '03', '06',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '0.0000001')}),
                      ('2018-03-06/PT2.0000048S',
                       {'start': DateTuple('2018', '03', '06',
                                           None, None, None),
                        'duration': DurationTuple(None, None, None,
                                                  None, None, None,
                                                  '2.0000048')}),
                      ('1980-03-05T01:01:00/1981-04-05T01:01:00',
                       {'start': DatetimeTuple(DateTuple('1980', '03', '05',
                                                         None, None, None),
                                               TimeTuple('01', '01', '00',
                                                         None)),
                        'end': DatetimeTuple(DateTuple('1981', '04', '05',
                                                       None, None, None),
                                             TimeTuple('01', '01', '00',
                                                       None))}),
                      ('1980-03-05T01:01:00/1981-04-05',
                       {'start': DatetimeTuple(DateTuple('1980', '03', '05',
                                                         None, None, None),
                                               TimeTuple('01', '01', '00',
                                                         None)),
                        'end': DateTuple('1981', '04', '05',
                                         None, None, None)}),
                      ('1980-03-05/1981-04-05T01:01:00',
                       {'start': DateTuple('1980', '03', '05',
                                           None, None, None),
                        'end': DatetimeTuple(DateTuple('1981', '04', '05',
                                                       None, None, None),
                                             TimeTuple('01', '01', '00',
                                                       None))}),
                      ('1980-03-05/1981-04-05',
                       {'start': DateTuple('1980', '03', '05',
                                           None, None, None),
                        'end': DateTuple('1981', '04', '05',
                                         None, None, None)}),
                      ('1981-04-05/1980-03-05',
                       {'start': DateTuple('1981', '04', '05',
                                           None, None, None),
                        'end': DateTuple('1980', '03', '05',
                                         None, None, None)}),
                      #Test concise interval
                      ('2020-01-01/02',
                       {'start': DateTuple('2020', '01', '01',
                                           None, None, None),
                        'end': DateTuple(None, None, '02',
                                         None, None, None)}),
                      ('2008-02-15/03-14',
                       {'start': DateTuple('2008', '02', '15',
                                           None, None, None),
                        'end': DateTuple(None, '03', '14',
                                         None, None, None)}),
                      ('2007-12-14T13:30/15:30',
                       {'start': DatetimeTuple(DateTuple('2007', '12', '14',
                                                         None, None, None),
                                               TimeTuple('13', '30', None,
                                                         None)),
                        'end': TimeTuple('15', '30', None,
                                         None)}),
                      ('2007-11-13T09:00/15T17:00',
                       {'start': DatetimeTuple(DateTuple('2007', '11', '13',
                                                         None, None, None),
                                               TimeTuple('09', '00', None,
                                                         None)),
                        'end': DatetimeTuple(DateTuple(None, None, '15',
                                                       None, None, None),
                                             TimeTuple('17', '00', None,
                                                       None))}),
                      ('2007-11-13T00:00/16T00:00',
                       {'start': DatetimeTuple(DateTuple('2007', '11', '13',
                                                         None, None, None),
                                               TimeTuple('00', '00', None,
                                                         None)),
                        'end': DatetimeTuple(DateTuple(None, None, '16',
                                                       None, None, None),
                                             TimeTuple('00', '00', None,
                                                       None))}),
                      ('2007-11-13T09:00Z/15T17:00',
                       {'start': DatetimeTuple(DateTuple('2007', '11', '13',
                                                         None, None, None),
                                               TimeTuple('09', '00', None,
                                                         TimezoneTuple(False,
                                                                       True,
                                                                       None,
                                                                       None,
                                                                       'Z'))),
                        'end': DatetimeTuple(DateTuple(None, None, '15',
                                                       None, None, None),
                                             TimeTuple('17', '00', None,
                                                       None))}),
                      ('2007-11-13T00:00/12:34.567',
                       {'start': DatetimeTuple(DateTuple('2007', '11', '13',
                                                         None, None, None),
                                               TimeTuple('00', '00', None,
                                                         None)),
                        'end': TimeTuple('12', '34.567', None,
                                         None)}),
                      #Make sure we truncate, not round
                      #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
                      ('1980-03-05T01:01:00.0000001/'
                       '1981-04-05T14:43:59.9999997',
                       {'start': DatetimeTuple(DateTuple('1980', '03', '05',
                                                         None, None, None),
                                               TimeTuple('01', '01', '00.0000001',
                                                         None)),
                        'end': DatetimeTuple(DateTuple('1981', '04', '05',
                                                       None, None, None),
                                             TimeTuple('14', '43', '59.9999997',
                                                       None))}))

        for testtuple in testtuples:
            mockBuilder = mock.Mock()
            mockBuilder.build_interval.return_value = testtuple[1]

            result = _parse_interval(testtuple[0], mockBuilder)

            self.assertEqual(result, testtuple[1])
            mockBuilder.build_interval.assert_called_once_with(**testtuple[1])

        #Test different separators
        expectedargs = {'start': DatetimeTuple(DateTuple('1980', '03', '05',
                                                         None, None, None),
                                               TimeTuple('01', '01', '00',
                                                         None)),
                        'end': DatetimeTuple(DateTuple('1981', '04', '05',
                                                       None, None, None),
                                             TimeTuple('01', '01', '00',
                                                       None))}

        mockBuilder = mock.Mock()
        mockBuilder.build_interval.return_value = expectedargs

        result = _parse_interval('1980-03-05T01:01:00--1981-04-05T01:01:00',
                                 mockBuilder,
                                 intervaldelimiter='--')

        self.assertEqual(result, expectedargs)
        mockBuilder.build_interval.assert_called_once_with(**expectedargs)

        expectedargs = {'start': DatetimeTuple(DateTuple('1980', '03', '05',
                                                         None, None, None),
                                  TimeTuple('01', '01', '00',
                                            None)),
                        'end': DatetimeTuple(DateTuple('1981', '04', '05',
                                                       None, None, None),
                                             TimeTuple('01', '01', '00',
                                                       None))}

        mockBuilder = mock.Mock()
        mockBuilder.build_interval.return_value = expectedargs

        _parse_interval('1980-03-05 01:01:00/1981-04-05 01:01:00',
                        mockBuilder,
                        datetimedelimiter=' ')

        self.assertEqual(result, expectedargs)
        mockBuilder.build_interval.assert_called_once_with(**expectedargs)

    def test_parse_interval_end(self):
        self.assertEqual(_parse_interval_end('02', DateTuple('2020', '01', '01',
                                                             None, None, None),
                                             'T'),
                                             DateTuple(None, None, '02',
                                                       None, None, None))

        self.assertEqual(_parse_interval_end('03-14', DateTuple('2008', '02', '15',
                                                                None, None, None),
                                             'T'),
                                             DateTuple(None, '03', '14',
                                                       None, None, None))

        self.assertEqual(_parse_interval_end('15:30', DatetimeTuple(DateTuple('2007', '12', '14',
                                                                              None, None, None),
                                                                    TimeTuple('13', '30', None,
                                                                              None)),
                                             'T'),
                                             TimeTuple('15', '30', None,
                                                       None))

        self.assertEqual(_parse_interval_end('15T17:00', DatetimeTuple(DateTuple('2007', '11', '13',
                                                                                 None, None, None),
                                                                       TimeTuple('09', '00', None,
                                                                                 None)),
                                             'T'),
                                             DatetimeTuple(DateTuple(None, None, '15',
                                                                     None, None, None),
                                                           TimeTuple('17', '00', None,
                                                                     None)))

        self.assertEqual(_parse_interval_end('16T00:00', DatetimeTuple(DateTuple('2007', '11', '13',
                                                                                 None, None, None),
                                                                       TimeTuple('00', '00', None,
                                                                                 None)),
                                             'T'),
                                             DatetimeTuple(DateTuple(None, None, '16',
                                                                     None, None, None),
                                                           TimeTuple('00', '00', None,
                                                                     None)))

        self.assertEqual(_parse_interval_end('15 17:00', DatetimeTuple(DateTuple('2007', '11', '13',
                                                                                 None, None, None),
                                                                       TimeTuple('09', '00', None,
                                                                                 None)),
                                             ' '),
                                             DatetimeTuple(DateTuple(None, None, '15',
                                                                     None, None, None),
                                                           TimeTuple('17', '00', None,
                                                                     None)))

class TestRepeatingIntervalParserFunctions(unittest.TestCase):
    def test_parse_repeating_interval(self):
        with mock.patch.object(aniso8601.interval.PythonTimeBuilder,
                               'build_repeating_interval') as mockBuilder:
            expectedargs = {'R': False, 'Rnn': '3',
                            'interval': IntervalTuple(DateTuple('1981', '04',
                                                                '05', None,
                                                                None, None),
                                                      None,
                                                      DurationTuple(None, None,
                                                                    None, '1',
                                                                    None, None,
                                                                    None))}

            mockBuilder.return_value = expectedargs

            result = parse_repeating_interval('R3/1981-04-05/P1D')

            self.assertEqual(result, expectedargs)
            mockBuilder.assert_called_once_with(**expectedargs)

        with mock.patch.object(aniso8601.interval.PythonTimeBuilder,
                               'build_repeating_interval') as mockBuilder:
            expectedargs = {'R': False, 'Rnn': '11',
                            'interval': IntervalTuple(None,
                                                      DatetimeTuple(DateTuple('1980', '03', '05',
                                                                              None, None, None),
                                                      TimeTuple('01', '01', '00',
                                                                None)),
                                                      DurationTuple(None, None, None,
                                                                    None, '1', '2',
                                                                    None))}

            mockBuilder.return_value = expectedargs

            result = parse_repeating_interval('R11/PT1H2M/1980-03-05T01:01:00')

            self.assertEqual(result, expectedargs)
            mockBuilder.assert_called_once_with(**expectedargs)

        with mock.patch.object(aniso8601.interval.PythonTimeBuilder,
                               'build_repeating_interval') as mockBuilder:
            expectedargs = {'R': False, 'Rnn': '2',
                            'interval': IntervalTuple(DatetimeTuple(DateTuple('1980', '03', '05',
                                                                              None, None, None),
                                                      TimeTuple('01', '01', '00',
                                                                None)),
                                                      DatetimeTuple(DateTuple('1981', '04', '05',
                                                                              None, None, None),
                                                      TimeTuple('01', '01', '00',
                                                                None)),
                                                      None)}

            mockBuilder.return_value = expectedargs

            result = parse_repeating_interval('R2--1980-03-05T01:01:00--'
                                              '1981-04-05T01:01:00',
                                              intervaldelimiter='--')

            self.assertEqual(result, expectedargs)
            mockBuilder.assert_called_once_with(**expectedargs)

        with mock.patch.object(aniso8601.interval.PythonTimeBuilder,
                               'build_repeating_interval') as mockBuilder:
            expectedargs = {'R': False, 'Rnn': '2',
                            'interval': IntervalTuple(DatetimeTuple(DateTuple('1980', '03', '05',
                                                                              None, None, None),
                                                                    TimeTuple('01', '01', '00',
                                                                              None)),
                                                      DatetimeTuple(DateTuple('1981', '04', '05',
                                                                              None, None, None),
                                                                    TimeTuple('01', '01', '00',
                                                                              None)),
                                                      None)}

            mockBuilder.return_value = expectedargs

            result = parse_repeating_interval('R2/'
                                              '1980-03-05 01:01:00/'
                                              '1981-04-05 01:01:00',
                                              datetimedelimiter=' ')

            self.assertEqual(result, expectedargs)
            mockBuilder.assert_called_once_with(**expectedargs)

        with mock.patch.object(aniso8601.interval.PythonTimeBuilder,
                               'build_repeating_interval') as mockBuilder:
            expectedargs = {'R': True, 'Rnn': None,
                            'interval': IntervalTuple(None,
                                                      DatetimeTuple(DateTuple('1980', '03', '05',
                                                                              None, None, None),
                                                                    TimeTuple('01', '01', '00',
                                                                              None)),
                                                      DurationTuple(None, None, None,
                                                                    None, '1', '2',
                                                                    None))}

            mockBuilder.return_value = expectedargs

            result = parse_repeating_interval('R/PT1H2M/1980-03-05T01:01:00')

            self.assertEqual(result, expectedargs)
            mockBuilder.assert_called_once_with(**expectedargs)

    def test_parse_repeating_interval_mockbuilder(self):
        mockBuilder = mock.Mock()

        args = {'R': False, 'Rnn': '3',
                'interval': IntervalTuple(DateTuple('1981', '04', '05',
                                                    None, None, None),
                             None,
                             DurationTuple(None, None, None, '1',
                                           None, None, None))}

        mockBuilder.build_repeating_interval.return_value = args

        result = parse_repeating_interval('R3/1981-04-05/P1D',
                                          builder=mockBuilder)

        self.assertEqual(result, args)
        mockBuilder.build_repeating_interval.assert_called_once_with(**args)

        mockBuilder = mock.Mock()

        args = {'R': False, 'Rnn': '11',
                'interval': IntervalTuple(None,
                                          DatetimeTuple(DateTuple('1980',
                                                                  '03', '05',
                                                                  None, None,
                                                                  None),
                                                        TimeTuple('01', '01',
                                                                  '00', None)),
                                          DurationTuple(None, None, None, None,
                                                        '1', '2', None))}

        mockBuilder.build_repeating_interval.return_value = args

        result = parse_repeating_interval('R11/PT1H2M/1980-03-05T01:01:00',
                                          builder=mockBuilder)

        self.assertEqual(result, args)
        mockBuilder.build_repeating_interval.assert_called_once_with(**args)

        mockBuilder = mock.Mock()

        args = {'R': True, 'Rnn': None,
                'interval': IntervalTuple(None,
                                          DatetimeTuple(DateTuple('1980', '03',
                                                                  '05', None,
                                                                  None, None),
                                                        TimeTuple('01', '01',
                                                                  '00', None)),
                                                        DurationTuple(None,
                                                                      None,
                                                                      None,
                                                                      None,
                                                                      '1', '2',
                                                                      None))}

        mockBuilder.build_repeating_interval.return_value = args

        result = parse_repeating_interval('R/PT1H2M/1980-03-05T01:01:00',
                                          builder=mockBuilder)

        self.assertEqual(result, args)
        mockBuilder.build_repeating_interval.assert_called_once_with(**args)

    def test_parse_repeating_interval_badtype(self):
        testtuples = (None, 1, False, 1.234)

        for testtuple in testtuples:
            with self.assertRaises(ValueError):
                parse_repeating_interval(testtuple, builder=None)

    def test_parse_repeating_interval_baddelimiter(self):
        testtuples = ('R,PT1H2M,1980-03-05T01:01:00', 'R3 1981-04-05 P1D')

        for testtuple in testtuples:
            with self.assertRaises(ISOFormatError):
                parse_repeating_interval(testtuple, builder=None)

    def test_parse_repeating_interval_suffixgarbage(self):
        #Don't allow garbage after the duration
        #https://bitbucket.org/nielsenb/aniso8601/issues/9/durations-with-trailing-garbage-are-parsed
        with self.assertRaises(ISOFormatError):
            parse_repeating_interval('R3/1981-04-05/P1Dasdf', builder=None)

        with self.assertRaises(ISOFormatError):
            parse_repeating_interval('R3/'
                                     '1981-04-05/'
                                     'P0003-06-04T12:30:05.5asdfasdf',
                                     builder=None)

    def test_parse_repeating_interval_badstr(self):
        testtuples = ('bad', '')

        for testtuple in testtuples:
            with self.assertRaises(ISOFormatError):
                parse_repeating_interval(testtuple, builder=None)
