# -*- coding: utf-8 -*-

# Copyright (c) 2018, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime
import unittest
import dateutil

from aniso8601.exceptions import ISOFormatError, RelativeValueError
from aniso8601.builder import NoneBuilder
from aniso8601.duration import parse_duration, _parse_duration_prescribed, \
        _parse_duration_combined, _parse_duration_prescribed_notime, \
        _parse_duration_prescribed_time, _parse_duration_element, \
        _has_any_component, _component_order_correct

class TestDurationParserFunctions(unittest.TestCase):
    def test_parse_duration(self):
        resultduration = parse_duration('P1Y2M3DT4H54M6S', builder=NoneBuilder)
        self.assertEqual(resultduration, ('1', '2', None, '3', '4', '54', '6'))

        resultduration = parse_duration('P1Y2M3DT4H54M6.5S', builder=NoneBuilder)
        self.assertEqual(resultduration, ('1', '2', None, '3', '4', '54', '6.5'))

        resultduration = parse_duration('P1Y2M3DT4H54M6,5S', builder=NoneBuilder)
        self.assertEqual(resultduration, ('1', '2', None, '3', '4', '54', '6.5'))

        resultduration = parse_duration('P1Y2M3D', builder=NoneBuilder)
        self.assertEqual(resultduration, ('1', '2', None, '3', None, None, None))

        resultduration = parse_duration('P1Y2M3.5D', builder=NoneBuilder)
        self.assertEqual(resultduration, ('1', '2', None, '3.5', None, None, None))

        resultduration = parse_duration('P1Y2M3,5D', builder=NoneBuilder)
        self.assertEqual(resultduration, ('1', '2', None, '3.5', None, None, None))

        resultduration = parse_duration('PT4H54M6.5S', builder=NoneBuilder)
        self.assertEqual(resultduration, (None, None, None, None, '4', '54', '6.5'))

        resultduration = parse_duration('PT4H54M6,5S', builder=NoneBuilder)
        self.assertEqual(resultduration, (None, None, None, None, '4', '54', '6.5'))

        resultduration = parse_duration('PT0.0000001S', builder=NoneBuilder)
        self.assertEqual(resultduration, (None, None, None, None, None, None, '0.0000001'))

        resultduration = parse_duration('PT2.0000048S', builder=NoneBuilder)
        self.assertEqual(resultduration, (None, None, None, None, None, None, '2.0000048'))

        resultduration = parse_duration('P1Y', builder=NoneBuilder)
        self.assertEqual(resultduration, ('1', None, None, None, None, None, None))

        resultduration = parse_duration('P1.5Y', builder=NoneBuilder)
        self.assertEqual(resultduration, ('1.5', None, None, None, None, None, None))

        resultduration = parse_duration('P1,5Y', builder=NoneBuilder)
        self.assertEqual(resultduration, ('1.5', None, None, None, None, None, None))

        resultduration = parse_duration('P1M', builder=NoneBuilder)
        self.assertEqual(resultduration, (None, '1', None, None, None, None, None))

        resultduration = parse_duration('P1.5M', builder=NoneBuilder)
        self.assertEqual(resultduration, (None, '1.5', None, None, None, None, None))

        resultduration = parse_duration('P1,5M', builder=NoneBuilder)
        self.assertEqual(resultduration, (None, '1.5', None, None, None, None, None))

        resultduration = parse_duration('P1W', builder=NoneBuilder)
        self.assertEqual(resultduration, (None, None, '1', None, None, None, None))

        resultduration = parse_duration('P1.5W', builder=NoneBuilder)
        self.assertEqual(resultduration, (None, None, '1.5', None, None, None, None))

        resultduration = parse_duration('P1,5W', builder=NoneBuilder)
        self.assertEqual(resultduration, (None, None, '1.5', None, None, None, None))

        resultduration = parse_duration('P1D', builder=NoneBuilder)
        self.assertEqual(resultduration, (None, None, None, '1', None, None, None))

        resultduration = parse_duration('P1.5D', builder=NoneBuilder)
        self.assertEqual(resultduration, (None, None, None, '1.5', None, None, None))

        resultduration = parse_duration('P1,5D', builder=NoneBuilder)
        self.assertEqual(resultduration, (None, None, None, '1.5', None, None, None))

        resultduration = parse_duration('P0003-06-04T12:30:05', builder=NoneBuilder)
        self.assertEqual(resultduration, ('0003', '06', None, '04', '12', '30', '05'))

        resultduration = parse_duration('P0003-06-04T12:30:05.5', builder=NoneBuilder)
        self.assertEqual(resultduration, ('0003', '06', None, '04', '12', '30', '05.5'))

        resultduration = parse_duration('P0001-02-03T14:43:59.9999997', builder=NoneBuilder)
        self.assertEqual(resultduration, ('0001', '02', None, '03', '14', '43', '59.9999997'))

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
        resultduration = _parse_duration_prescribed('P1Y2M3DT4H54M6S', NoneBuilder)
        self.assertEqual(resultduration, ('1', '2', None, '3', '4', '54', '6'))

        resultduration = _parse_duration_prescribed('P1Y2M3DT4H54M6.5S', NoneBuilder)
        self.assertEqual(resultduration, ('1', '2', None, '3', '4', '54', '6.5'))

        resultduration = _parse_duration_prescribed('P1Y2M3DT4H54M6,5S', NoneBuilder)
        self.assertEqual(resultduration, ('1', '2', None, '3', '4', '54', '6.5'))

        resultduration = _parse_duration_prescribed('PT4H54M6.5S', NoneBuilder)
        self.assertEqual(resultduration, (None, None, None, None, '4', '54', '6.5'))

        resultduration = _parse_duration_prescribed('PT4H54M6,5S', NoneBuilder)
        self.assertEqual(resultduration, (None, None, None, None, '4', '54', '6.5'))

        resultduration = _parse_duration_prescribed('P1Y2M3D', NoneBuilder)
        self.assertEqual(resultduration, ('1', '2', None, '3', None, None, None))

        resultduration = _parse_duration_prescribed('P1Y2M3.5D', NoneBuilder)
        self.assertEqual(resultduration, ('1', '2', None, '3.5', None, None, None))

        resultduration = _parse_duration_prescribed('P1Y2M3,5D', NoneBuilder)
        self.assertEqual(resultduration, ('1', '2', None, '3.5', None, None, None))

        resultduration = _parse_duration_prescribed('P1Y', NoneBuilder)
        self.assertEqual(resultduration, ('1', None, None, None, None, None, None))

        resultduration = _parse_duration_prescribed('P1.5Y', NoneBuilder)
        self.assertEqual(resultduration, ('1.5', None, None, None, None, None, None))

        resultduration = _parse_duration_prescribed('P1,5Y', NoneBuilder)
        self.assertEqual(resultduration, ('1.5', None, None, None, None, None, None))

        resultduration = _parse_duration_prescribed('P1M', NoneBuilder)
        self.assertEqual(resultduration, (None, '1', None, None, None, None, None))

        resultduration = _parse_duration_prescribed('P1.5M', NoneBuilder)
        self.assertEqual(resultduration, (None, '1.5', None, None, None, None, None))

        resultduration = _parse_duration_prescribed('P1,5M', NoneBuilder)
        self.assertEqual(resultduration, (None, '1.5', None, None, None, None, None))

        resultduration = _parse_duration_prescribed('P1W', NoneBuilder)
        self.assertEqual(resultduration, (None, None, '1', None, None, None, None))

        resultduration = _parse_duration_prescribed('P1.5W', NoneBuilder)
        self.assertEqual(resultduration, (None, None, '1.5', None, None, None, None))

        resultduration = _parse_duration_prescribed('P1,5W', NoneBuilder)
        self.assertEqual(resultduration, (None, None, '1.5', None, None, None, None))

        resultduration = _parse_duration_prescribed('P1D', NoneBuilder)
        self.assertEqual(resultduration, (None, None, None, '1', None, None, None))

        resultduration = _parse_duration_prescribed('P1.5D', NoneBuilder)
        self.assertEqual(resultduration, (None, None, None, '1.5', None, None, None))

        resultduration = _parse_duration_prescribed('P1,5D', NoneBuilder)
        self.assertEqual(resultduration, (None, None, None, '1.5', None, None, None))

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
        resultduration = _parse_duration_combined('P0003-06-04T12:30:05', NoneBuilder)
        self.assertEqual(resultduration, ('0003', '06', None, '04', '12', '30', '05'))

        resultduration = _parse_duration_combined('P0003-06-04T12:30:05.5', NoneBuilder)
        self.assertEqual(resultduration, ('0003', '06', None, '04', '12', '30', '05.5'))

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

class TestRelativeDurationParserFunctions(unittest.TestCase):
    def test_parse_duration_relative(self):
        resultduration = parse_duration('P1Y2M3DT4H54M6.5S', relative=True)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(years=1, months=2, days=3, hours=4, minutes=54, seconds=6, microseconds=500000))

        resultduration = parse_duration('P0003-06-04T12:30:05.5', relative=True)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(years=3, months=6, days=4, hours=12, minutes=30, seconds=5, microseconds=500000))

        #Make sure we truncate, not round
        #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
        resultduration = parse_duration('P0001-02-03T14:43:59.9999997', relative=True)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(years=1, months=2, days=3, hours=14, minutes=43, seconds=59, microseconds=999999))

    def test_parse_duration_prescribed_relative(self):
        resultduration = _parse_duration_prescribed('P1Y', True)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(years=1))

        resultduration = _parse_duration_prescribed('P1M', True)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(months=1))

        #Add the relative ‘days’ argument to the absolute day. Notice that the ‘weeks’ argument is multiplied by 7 and added to ‘days’.
        #http://dateutil.readthedocs.org/en/latest/relativedelta.html
        resultduration = _parse_duration_prescribed('P1W', True)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(days=7))

        resultduration = _parse_duration_prescribed('P1.5W', True)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(days=10.5))

        #Make sure we truncate, not round
        #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
        resultduration = parse_duration('PT0.0000001S', relative=True)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(0))

        resultduration = parse_duration('PT2.0000048S', relative=True)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(seconds=2, microseconds=4))

    def test_parse_duration_prescribed_relative_multiplefractions(self):
        with self.assertRaises(ISOFormatError):
            #Multiple fractions are not allowed
            _parse_duration_prescribed('P1Y2M3DT4H5.1234M6.1234S', True)

    def test_parse_duration_prescribed_relative_middlefraction(self):
        with self.assertRaises(ISOFormatError):
            #Fraction only allowed on final component
            _parse_duration_prescribed('P1Y2M3DT4H5.1234M6S', True)

    def test_parse_duration_prescribed_relative_suffixgarbage(self):
        #Don't allow garbage after the duration
        #https://bitbucket.org/nielsenb/aniso8601/issues/9/durations-with-trailing-garbage-are-parsed
        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed('P1Dasdfasdf', True)

    def test_parse_duration_prescribed_relative_fractionalyear(self):
        #Fractional months and years are not defined
        #https://github.com/dateutil/dateutil/issues/40
        with self.assertRaises(RelativeValueError):
            _parse_duration_prescribed('P1.5Y', True)

    def test_parse_duration_prescribed_relative_fractionalmonth(self):
        #Fractional months and years are not defined
        #https://github.com/dateutil/dateutil/issues/40
        with self.assertRaises(RelativeValueError):
            _parse_duration_prescribed('P1.5M', True)

    def test_parse_duration_prescribed_relative_outoforder(self):
        #Ensure durations are required to be in the correct order
        #https://bitbucket.org/nielsenb/aniso8601/issues/7/durations-with-time-components-before-t
        #https://bitbucket.org/nielsenb/aniso8601/issues/8/durations-with-components-in-wrong-order
        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed('P1S', True)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed('P1D1S', True)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed('P1H1M', True)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed('1Y2M3D1SPT1M', True)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed('P1Y2M3D2MT1S', True)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed('P2M3D1ST1Y1M', True)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed('P1Y2M2MT3D1S', True)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed('P1D1Y1M', True)

        with self.assertRaises(ISOFormatError):
            _parse_duration_prescribed('PT1S1H', True)

    def test_parse_duration_prescribed_relative_nodateutil(self):
        import sys
        import dateutil

        dateutil_import = dateutil

        sys.modules['dateutil'] = None

        with self.assertRaises(RuntimeError):
            _parse_duration_prescribed('P1Y', True)

        #Reinstall dateutil
        sys.modules['dateutil'] = dateutil

    def test_parse_duration_prescribed_notime_RelativeTimeBuilder(self):
        resultduration = _parse_duration_prescribed_notime('P1Y2M3D', RelativeTimeBuilder)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(years=1, months=2, days=3))

        resultduration = _parse_duration_prescribed_notime('P1Y2M3.5D', RelativeTimeBuilder)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(years=1, months=2, days=3.5))

        resultduration = _parse_duration_prescribed_notime('P1Y2M3,5D', RelativeTimeBuilder)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(years=1, months=2, days=3.5))

        resultduration = _parse_duration_prescribed_notime('P1Y', RelativeTimeBuilder)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(years=1))

        resultduration = _parse_duration_prescribed_notime('P1M', RelativeTimeBuilder)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(months=1))

        resultduration = _parse_duration_prescribed_notime('P1W', RelativeTimeBuilder)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(days=7))

        resultduration = _parse_duration_prescribed_notime('P1.5W', RelativeTimeBuilder)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(days=10.5))

        resultduration = _parse_duration_prescribed_notime('P1,5W', RelativeTimeBuilder)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(days=10.5))

        resultduration = _parse_duration_prescribed_notime('P1D', RelativeTimeBuilder)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(days=1))

        resultduration = _parse_duration_prescribed_notime('P1.5D', RelativeTimeBuilder)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(days=1.5))

        resultduration = _parse_duration_prescribed_notime('P1,5D', RelativeTimeBuilder)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(days=1.5))

    def test_parse_duration_prescribed_time_RelativeTimeBuilder(self):
        resultduration = _parse_duration_prescribed_time('P1Y2M3DT4H54M6S', RelativeTimeBuilder)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(years=1, months=2, days=3, hours=4, minutes=54, seconds=6))

        resultduration = _parse_duration_prescribed_time('P1Y2M3DT4H54M6.5S', RelativeTimeBuilder)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(years=1, months=2, days=3, hours=4, minutes=54, seconds=6, microseconds=500000))

        resultduration = _parse_duration_prescribed_time('P1Y2M3DT4H54M6,5S', RelativeTimeBuilder)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(years=1, months=2, days=3, hours=4, minutes=54, seconds=6, microseconds=500000))

        resultduration = _parse_duration_prescribed_time('PT4H54M6.5S', RelativeTimeBuilder)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(hours=4, minutes=54, seconds=6, microseconds=500000))

        resultduration = _parse_duration_prescribed_time('PT4H54M6,5S', RelativeTimeBuilder)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(hours=4, minutes=54, seconds=6, microseconds=500000))

    def test_parse_duration_combined_relative(self):
        resultduration = _parse_duration_combined('P0003-06-04T12:30:05', True)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(years=3, months=6, days=4, hours=12, minutes=30, seconds=5))

        resultduration = _parse_duration_combined('P0003-06-04T12:30:05.5', True)
        self.assertEqual(resultduration, dateutil.relativedelta.relativedelta(years=3, months=6, days=4, hours=12, minutes=30, seconds=5, microseconds=500000))

    def test_parse_duration_combined_relative_suffixgarbage(self):
        #Don't allow garbage after the duration
        #https://bitbucket.org/nielsenb/aniso8601/issues/9/durations-with-trailing-garbage-are-parsed
        with self.assertRaises(ISOFormatError):
            _parse_duration_combined('P0003-06-04T12:30:05.5asdfasdf', True)

    def test_parse_duration_combined_relative_nodateutil(self):
        import sys
        import dateutil

        dateutil_import = dateutil

        sys.modules['dateutil'] = None

        with self.assertRaises(RuntimeError):
            _parse_duration_combined('P0003-06-04T12:30:05', True)

        #Reinstall dateutil
        sys.modules['dateutil'] = dateutil
