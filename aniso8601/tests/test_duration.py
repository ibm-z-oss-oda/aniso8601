# -*- coding: utf-8 -*-

# Copyright (c) 2018, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import unittest

from aniso8601.exceptions import ISOFormatError
from aniso8601.builder import NoneBuilder
from aniso8601.duration import parse_duration, _parse_duration_prescribed, \
        _parse_duration_combined, _parse_duration_prescribed_notime, \
        _parse_duration_prescribed_time, _parse_duration_element, \
        _has_any_component, _component_order_correct

class TestDurationParserFunctions(unittest.TestCase):
    def test_parse_duration(self):
        parse = parse_duration('P1Y2M3DT4H54M6S', builder=NoneBuilder)
        self.assertEqual(parse, ('1', '2', None, '3', '4', '54', '6', 'duration'))

        parse = parse_duration('P1Y2M3DT4H54M6.5S', builder=NoneBuilder)
        self.assertEqual(parse, ('1', '2', None, '3', '4', '54', '6.5', 'duration'))

        parse = parse_duration('P1Y2M3DT4H54M6,5S', builder=NoneBuilder)
        self.assertEqual(parse, ('1', '2', None, '3', '4', '54', '6.5', 'duration'))

        parse = parse_duration('P1Y2M3D', builder=NoneBuilder)
        self.assertEqual(parse, ('1', '2', None, '3', None, None, None, 'duration'))

        parse = parse_duration('P1Y2M3.5D', builder=NoneBuilder)
        self.assertEqual(parse, ('1', '2', None, '3.5', None, None, None, 'duration'))

        parse = parse_duration('P1Y2M3,5D', builder=NoneBuilder)
        self.assertEqual(parse, ('1', '2', None, '3.5', None, None, None, 'duration'))

        parse = parse_duration('PT4H54M6.5S', builder=NoneBuilder)
        self.assertEqual(parse, (None, None, None, None, '4', '54', '6.5', 'duration'))

        parse = parse_duration('PT4H54M6,5S', builder=NoneBuilder)
        self.assertEqual(parse, (None, None, None, None, '4', '54', '6.5', 'duration'))

        parse = parse_duration('PT0.0000001S', builder=NoneBuilder)
        self.assertEqual(parse, (None, None, None, None, None, None, '0.0000001', 'duration'))

        parse = parse_duration('PT2.0000048S', builder=NoneBuilder)
        self.assertEqual(parse, (None, None, None, None, None, None, '2.0000048', 'duration'))

        parse = parse_duration('P1Y', builder=NoneBuilder)
        self.assertEqual(parse, ('1', None, None, None, None, None, None, 'duration'))

        parse = parse_duration('P1.5Y', builder=NoneBuilder)
        self.assertEqual(parse, ('1.5', None, None, None, None, None, None, 'duration'))

        parse = parse_duration('P1,5Y', builder=NoneBuilder)
        self.assertEqual(parse, ('1.5', None, None, None, None, None, None, 'duration'))

        parse = parse_duration('P1M', builder=NoneBuilder)
        self.assertEqual(parse, (None, '1', None, None, None, None, None, 'duration'))

        parse = parse_duration('P1.5M', builder=NoneBuilder)
        self.assertEqual(parse, (None, '1.5', None, None, None, None, None, 'duration'))

        parse = parse_duration('P1,5M', builder=NoneBuilder)
        self.assertEqual(parse, (None, '1.5', None, None, None, None, None, 'duration'))

        parse = parse_duration('P1W', builder=NoneBuilder)
        self.assertEqual(parse, (None, None, '1', None, None, None, None, 'duration'))

        parse = parse_duration('P1.5W', builder=NoneBuilder)
        self.assertEqual(parse, (None, None, '1.5', None, None, None, None, 'duration'))

        parse = parse_duration('P1,5W', builder=NoneBuilder)
        self.assertEqual(parse, (None, None, '1.5', None, None, None, None, 'duration'))

        parse = parse_duration('P1D', builder=NoneBuilder)
        self.assertEqual(parse, (None, None, None, '1', None, None, None, 'duration'))

        parse = parse_duration('P1.5D', builder=NoneBuilder)
        self.assertEqual(parse, (None, None, None, '1.5', None, None, None, 'duration'))

        parse = parse_duration('P1,5D', builder=NoneBuilder)
        self.assertEqual(parse, (None, None, None, '1.5', None, None, None, 'duration'))

        parse = parse_duration('P0003-06-04T12:30:05', builder=NoneBuilder)
        self.assertEqual(parse, ('0003', '06', None, '04', '12', '30', '05', 'duration'))

        parse = parse_duration('P0003-06-04T12:30:05.5', builder=NoneBuilder)
        self.assertEqual(parse, ('0003', '06', None, '04', '12', '30', '05.5', 'duration'))

        parse = parse_duration('P0001-02-03T14:43:59.9999997', builder=NoneBuilder)
        self.assertEqual(parse, ('0001', '02', None, '03', '14', '43', '59.9999997', 'duration'))

    def test_parse_duration_nop(self):
        with self.assertRaises(ISOFormatError):
            #Duration must start with a P
            parse_duration('1Y2M3DT4H54M6S', builder=NoneBuilder)

    def test_parse_duration_weekcombination(self):
        with self.assertRaises(ISOFormatError):
            #Week designator cannot be combined with other time designators
            #https://bitbucket.org/nielsenb/aniso8601/issues/2/week-designators-should-not-be-combinable
            parse_duration('P1Y2W', builder=NoneBuilder)

    def test_parse_duration_outoforder(self):
        #Ensure durations are required to be in the correct order
        #https://bitbucket.org/nielsenb/aniso8601/issues/7/durations-with-time-components-before-t
        #https://bitbucket.org/nielsenb/aniso8601/issues/8/durations-with-components-in-wrong-order
        with self.assertRaises(ISOFormatError):
            parse_duration('P1S', builder=NoneBuilder)

        with self.assertRaises(ISOFormatError):
            parse_duration('P1D1S', builder=NoneBuilder)

        with self.assertRaises(ISOFormatError):
            parse_duration('P1H1M', builder=NoneBuilder)

        with self.assertRaises(ISOFormatError):
            parse_duration('1Y2M3D1SPT1M', builder=NoneBuilder)

        with self.assertRaises(ISOFormatError):
            parse_duration('P1Y2M3D2MT1S', builder=NoneBuilder)

        with self.assertRaises(ISOFormatError):
            parse_duration('P2M3D1ST1Y1M', builder=NoneBuilder)

        with self.assertRaises(ISOFormatError):
            parse_duration('P1Y2M2MT3D1S', builder=NoneBuilder)

        with self.assertRaises(ISOFormatError):
            parse_duration('P1D1Y1M', builder=NoneBuilder)

        with self.assertRaises(ISOFormatError):
            parse_duration('PT1S1H', builder=NoneBuilder)

    def test_parse_duration_prescribed(self):
        parse = _parse_duration_prescribed('P1Y2M3DT4H54M6S', NoneBuilder)
        self.assertEqual(parse, ('1', '2', None, '3', '4', '54', '6', 'duration'))

        parse = _parse_duration_prescribed('P1Y2M3DT4H54M6.5S', NoneBuilder)
        self.assertEqual(parse, ('1', '2', None, '3', '4', '54', '6.5', 'duration'))

        parse = _parse_duration_prescribed('P1Y2M3DT4H54M6,5S', NoneBuilder)
        self.assertEqual(parse, ('1', '2', None, '3', '4', '54', '6.5', 'duration'))

        parse = _parse_duration_prescribed('PT4H54M6.5S', NoneBuilder)
        self.assertEqual(parse, (None, None, None, None, '4', '54', '6.5', 'duration'))

        parse = _parse_duration_prescribed('PT4H54M6,5S', NoneBuilder)
        self.assertEqual(parse, (None, None, None, None, '4', '54', '6.5', 'duration'))

        parse = _parse_duration_prescribed('P1Y2M3D', NoneBuilder)
        self.assertEqual(parse, ('1', '2', None, '3', None, None, None, 'duration'))

        parse = _parse_duration_prescribed('P1Y2M3.5D', NoneBuilder)
        self.assertEqual(parse, ('1', '2', None, '3.5', None, None, None, 'duration'))

        parse = _parse_duration_prescribed('P1Y2M3,5D', NoneBuilder)
        self.assertEqual(parse, ('1', '2', None, '3.5', None, None, None, 'duration'))

        parse = _parse_duration_prescribed('P1Y', NoneBuilder)
        self.assertEqual(parse, ('1', None, None, None, None, None, None, 'duration'))

        parse = _parse_duration_prescribed('P1.5Y', NoneBuilder)
        self.assertEqual(parse, ('1.5', None, None, None, None, None, None, 'duration'))

        parse = _parse_duration_prescribed('P1,5Y', NoneBuilder)
        self.assertEqual(parse, ('1.5', None, None, None, None, None, None, 'duration'))

        parse = _parse_duration_prescribed('P1M', NoneBuilder)
        self.assertEqual(parse, (None, '1', None, None, None, None, None, 'duration'))

        parse = _parse_duration_prescribed('P1.5M', NoneBuilder)
        self.assertEqual(parse, (None, '1.5', None, None, None, None, None, 'duration'))

        parse = _parse_duration_prescribed('P1,5M', NoneBuilder)
        self.assertEqual(parse, (None, '1.5', None, None, None, None, None, 'duration'))

        parse = _parse_duration_prescribed('P1W', NoneBuilder)
        self.assertEqual(parse, (None, None, '1', None, None, None, None, 'duration'))

        parse = _parse_duration_prescribed('P1.5W', NoneBuilder)
        self.assertEqual(parse, (None, None, '1.5', None, None, None, None, 'duration'))

        parse = _parse_duration_prescribed('P1,5W', NoneBuilder)
        self.assertEqual(parse, (None, None, '1.5', None, None, None, None, 'duration'))

        parse = _parse_duration_prescribed('P1D', NoneBuilder)
        self.assertEqual(parse, (None, None, None, '1', None, None, None, 'duration'))

        parse = _parse_duration_prescribed('P1.5D', NoneBuilder)
        self.assertEqual(parse, (None, None, None, '1.5', None, None, None, 'duration'))

        parse = _parse_duration_prescribed('P1,5D', NoneBuilder)
        self.assertEqual(parse, (None, None, None, '1.5', None, None, None, 'duration'))

    def test_parse_duration_prescribed_multiplefractions(self):
        with self.assertRaises(ISOFormatError):
            #Multiple fractions are not allowed
            _parse_duration_prescribed('P1Y2M3DT4H5.1234M6.1234S', NoneBuilder)

    def test_parse_duration_prescribed_middlefraction(self):
        with self.assertRaises(ISOFormatError):
            #Fraction only allowed on final component
            _parse_duration_prescribed('P1Y2M3DT4H5.1234M6S', NoneBuilder)

    def test_parse_duration_prescribed_suffixgarbage(self):
        #Don't allow garbage after the duration
        #https://bitbucket.org/nielsenb/aniso8601/issues/9/durations-with-trailing-garbage-are-parsed
        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed('P1Dasdfasdf', NoneBuilder)

    def test_parse_duration_prescribed_outoforder(self):
        #Ensure durations are required to be in the correct order
        #https://bitbucket.org/nielsenb/aniso8601/issues/7/durations-with-time-components-before-t
        #https://bitbucket.org/nielsenb/aniso8601/issues/8/durations-with-components-in-wrong-order
        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed('P1S', NoneBuilder)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed('P1D1S', NoneBuilder)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed('P1H1M', NoneBuilder)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed('1Y2M3D1SPT1M', NoneBuilder)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed('P1Y2M3D2MT1S', NoneBuilder)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed('P2M3D1ST1Y1M', NoneBuilder)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed('P1Y2M2MT3D1S', NoneBuilder)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed('P1D1Y1M', NoneBuilder)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed('PT1S1H', NoneBuilder)

    def test_parse_duration_prescribed_notime(self):
        parse = _parse_duration_prescribed_notime('P1Y2M3D', NoneBuilder)
        self.assertEqual(parse, ('1', '2', None, '3', None, None, None, 'duration'))

        parse = _parse_duration_prescribed_notime('P1Y2M3.5D', NoneBuilder)
        self.assertEqual(parse, ('1', '2', None, '3.5', None, None, None, 'duration'))

        parse = _parse_duration_prescribed_notime('P1Y2M3,5D', NoneBuilder)
        self.assertEqual(parse, ('1', '2', None, '3.5', None, None, None, 'duration'))

        parse = _parse_duration_prescribed_notime('P1Y', NoneBuilder)
        self.assertEqual(parse, ('1', None, None, None, None, None, None, 'duration'))

        parse = _parse_duration_prescribed_notime('P1.5Y', NoneBuilder)
        self.assertEqual(parse, ('1.5', None, None, None, None, None, None, 'duration'))

        parse = _parse_duration_prescribed_notime('P1,5Y', NoneBuilder)
        self.assertEqual(parse, ('1.5', None, None, None, None, None, None, 'duration'))

        parse = _parse_duration_prescribed_notime('P1M', NoneBuilder)
        self.assertEqual(parse, (None, '1', None, None, None, None, None, 'duration'))

        parse = _parse_duration_prescribed_notime('P1.5M', NoneBuilder)
        self.assertEqual(parse, (None, '1.5', None, None, None, None, None, 'duration'))

        parse = _parse_duration_prescribed_notime('P1,5M', NoneBuilder)
        self.assertEqual(parse, (None, '1.5', None, None, None, None, None, 'duration'))

        parse = _parse_duration_prescribed_notime('P1W', NoneBuilder)
        self.assertEqual(parse, (None, None, '1', None, None, None, None, 'duration'))

        parse = _parse_duration_prescribed_notime('P1.5W', NoneBuilder)
        self.assertEqual(parse, (None, None, '1.5', None, None, None, None, 'duration'))

        parse = _parse_duration_prescribed_notime('P1,5W', NoneBuilder)
        self.assertEqual(parse, (None, None, '1.5', None, None, None, None, 'duration'))

        parse = _parse_duration_prescribed_notime('P1D', NoneBuilder)
        self.assertEqual(parse, (None, None, None, '1', None, None, None, 'duration'))

        parse = _parse_duration_prescribed_notime('P1.5D', NoneBuilder)
        self.assertEqual(parse, (None, None, None, '1.5', None, None, None, 'duration'))

        parse = _parse_duration_prescribed_notime('P1,5D', NoneBuilder)
        self.assertEqual(parse, (None, None, None, '1.5', None, None, None, 'duration'))

    def test_parse_duration_prescribed_notime_timepart(self):
        #Ensure no time part is allowed
        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed_notime('P1S', NoneBuilder)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed_notime('P1D1S', NoneBuilder)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed_notime('P1H1M', NoneBuilder)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed_notime('P1Y2M3D4H', NoneBuilder)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed_notime('P1Y2M3D4H5S', NoneBuilder)

    def test_parse_duration_prescribed_notime_outoforder(self):
        #Ensure durations are required to be in the correct order
        #https://bitbucket.org/nielsenb/aniso8601/issues/8/durations-with-components-in-wrong-order
        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed_notime('P1H1M', NoneBuilder)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed_notime('P1D1Y1M', NoneBuilder)

    def test_parse_duration_prescribed_time(self):
        parse = _parse_duration_prescribed_time('P1Y2M3DT4H54M6S', NoneBuilder)
        self.assertEqual(parse, ('1', '2', None, '3', '4', '54', '6', 'duration'))

        parse = _parse_duration_prescribed_time('P1Y2M3DT4H54M6.5S', NoneBuilder)
        self.assertEqual(parse, ('1', '2', None, '3', '4', '54', '6.5', 'duration'))

        parse = _parse_duration_prescribed_time('P1Y2M3DT4H54M6,5S', NoneBuilder)
        self.assertEqual(parse, ('1', '2', None, '3', '4', '54', '6.5', 'duration'))

        parse = _parse_duration_prescribed_time('PT4H54M6.5S', NoneBuilder)
        self.assertEqual(parse, (None, None, None, None, '4', '54', '6.5', 'duration'))

        parse = _parse_duration_prescribed_time('PT4H54M6,5S', NoneBuilder)
        self.assertEqual(parse, (None, None, None, None, '4', '54', '6.5', 'duration'))

    def test_parse_duration_prescribed_time_timeindate(self):
        #Don't allow time components in date half
        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed_time('P1Y2M3D4HT54M6S', NoneBuilder)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed_time('P1Y2M3D6ST4H54M', NoneBuilder)

    def test_parse_duration_prescribed_time_dateintime(self):
        #Don't allow date components in time half
        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed_time('P2M3DT1Y4H54M6S', NoneBuilder)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed_time('P1Y2MT3D4H54M6S', NoneBuilder)

    def test_parse_duration_prescribed_time_outoforder(self):
        #Ensure durations are required to be in the correct order
        #https://bitbucket.org/nielsenb/aniso8601/issues/7/durations-with-time-components-before-t
        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed_time('1Y2M3D1SPT1M', NoneBuilder)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed_time('P1Y2M3D2MT1S', NoneBuilder)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed_time('P2M3D1ST1Y1M', NoneBuilder)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed_time('P1Y2M2MT3D1S', NoneBuilder)

    def test_parse_duration_combined(self):
        parse = _parse_duration_combined('P0003-06-04T12:30:05', NoneBuilder)
        self.assertEqual(parse, ('0003', '06', None, '04', '12', '30', '05', 'duration'))

        parse = _parse_duration_combined('P0003-06-04T12:30:05.5', NoneBuilder)
        self.assertEqual(parse, ('0003', '06', None, '04', '12', '30', '05.5', 'duration'))

    def test_parse_duration_combined_suffixgarbage(self):
        #Don't allow garbage after the duration
        #https://bitbucket.org/nielsenb/aniso8601/issues/9/durations-with-trailing-garbage-are-parsed
        with self.assertRaises(ISOFormatError):
            _parse_duration_combined('P0003-06-04T12:30:05.5asdfasdf', NoneBuilder)

    def test_parse_duration_element(self):
        self.assertEqual(_parse_duration_element('P1Y2M3D', 'Y'), '1')
        self.assertEqual(_parse_duration_element('P1Y2M3D', 'M'), '2')
        self.assertEqual(_parse_duration_element('P1Y2M3D', 'D'), '3')
        self.assertEqual(_parse_duration_element('T4H5M6.1234S', 'H'), '4')
        self.assertEqual(_parse_duration_element('T4H5M6.1234S', 'M'), '5')
        self.assertEqual(_parse_duration_element('T4H5M6.1234S', 'S'), '6.1234')
        self.assertEqual(_parse_duration_element('PT4H54M6,5S', 'H'), '4')
        self.assertEqual(_parse_duration_element('PT4H54M6,5S', 'M'), '54')
        self.assertEqual(_parse_duration_element('PT4H54M6,5S', 'S'), '6.5')

    def test_has_any_component(self):
        self.assertTrue(_has_any_component('P1Y', ['Y', 'M']))
        self.assertFalse(_has_any_component('P1Y', ['M', 'D']))

    def test_component_order_correct(self):
        self.assertTrue(_component_order_correct('P1Y1M1D', ['P', 'Y', 'M', 'D']))
        self.assertTrue(_component_order_correct('P1Y1M', ['P', 'Y', 'M', 'D']))
        self.assertFalse(_component_order_correct('P1D1Y1M', ['P', 'Y', 'M', 'D']))
        self.assertFalse(_component_order_correct('PT1S1H', ['T', 'H', 'M', 'S']))
