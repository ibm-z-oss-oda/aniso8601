# -*- coding: utf-8 -*-

# Copyright (c) 2016, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime
import unittest
import dateutil.relativedelta

from aniso8601.builder import BaseTimeBuilder, PythonTimeBuilder, RelativeTimeBuilder
from aniso8601.timezone import UTCOffset

class TestBaseTimeBuilder(unittest.TestCase):
    def test_build_date(self):
        with self.assertRaises(NotImplementedError):
            BaseTimeBuilder.build_date(1, 2, 3)

    def test_build_time(self):
        with self.assertRaises(NotImplementedError):
            BaseTimeBuilder.build_time()

    def test_build_datetime(self):
        with self.assertRaises(NotImplementedError):
            BaseTimeBuilder.build_datetime(1, 2, 3)

    def test_build_timedelta(self):
        with self.assertRaises(NotImplementedError):
            BaseTimeBuilder.build_timedelta()

    def test_build_combine(self):
        with self.assertRaises(NotImplementedError):
            BaseTimeBuilder.combine(None, None)

class TestPythonTimeBuilder(unittest.TestCase):
    def test_build_date(self):
        self.assertEqual(PythonTimeBuilder.build_date(1, 2, 3), datetime.date(1, 2, 3))

    def test_build_time(self):
        time = PythonTimeBuilder.build_time()
        self.assertEqual(time, datetime.time())

        time = PythonTimeBuilder.build_time(hours=1, minutes=23)
        self.assertEqual(time, datetime.time(hour=1, minute=23))

        time = PythonTimeBuilder.build_time(hours=1, minutes=23.4567)
        self.assertEqual(time, datetime.time(hour=1, minute=23, second=27, microsecond=402000))

        time = PythonTimeBuilder.build_time(hours=23, minutes=21, seconds=28.512400)
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400))

        time = PythonTimeBuilder.build_time(hours=23, minutes=21, seconds=28, microseconds=512400)
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400))

        time = PythonTimeBuilder.build_time(tzinfo=UTCOffset(name='UTC', minutes=0))
        self.assertEqual(time, datetime.time(tzinfo=UTCOffset(name='UTC', minutes=0)))

        time = PythonTimeBuilder.build_time(hours=1, minutes=23, tzinfo=UTCOffset(name='+1', minutes=60))
        self.assertEqual(time, datetime.time(hour=1, minute=23, tzinfo=UTCOffset(name='+1', minutes=60)))

        time = PythonTimeBuilder.build_time(hours=1, minutes=23.4567, tzinfo=UTCOffset(name='-1', minutes=-60))
        self.assertEqual(time, datetime.time(hour=1, minute=23, second=27, microsecond=402000, tzinfo=UTCOffset(name='-1', minutes=-60)))

        time = PythonTimeBuilder.build_time(hours=23, minutes=21, seconds=28.512400, tzinfo=UTCOffset(name='+1.5', minutes=90))
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='+1.5', minutes=90)))

        time = PythonTimeBuilder.build_time(hours=23, minutes=21, seconds=28, microseconds=512400, tzinfo=UTCOffset(name='-1.5', minutes=-90))
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='-1.5', minutes=-90)))

    def test_build_datetime(self):
        resultdatetime = PythonTimeBuilder.build_datetime(1981, 4, 5)
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5))

        resultdatetime = PythonTimeBuilder.build_datetime(1981, 4, 5, hours=1, minutes=23.4567)
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=1, minute=23, second=27, microsecond=402000))

        resultdatetime = PythonTimeBuilder.build_datetime(1981, 4, 5, hours=23, minutes=21, seconds=28.512400)
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=23, minute=21, second=28, microsecond=512400))

        resultdatetime = PythonTimeBuilder.build_datetime(1981, 4, 5, hours=23, minutes=21, seconds=28, microseconds=512400)
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=23, minute=21, second=28, microsecond=512400))

        resultdatetime = PythonTimeBuilder.build_datetime(1981, 4, 5, tzinfo=UTCOffset(name='UTC', minutes=0))
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, tzinfo=UTCOffset(name='UTC', minutes=0)))

        resultdatetime = PythonTimeBuilder.build_datetime(1981, 4, 5, hours=1, minutes=23.4567, tzinfo=UTCOffset(name='+1', minutes=60))
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=1, minute=23, second=27, microsecond=402000, tzinfo=UTCOffset(name='+1', minutes=60)))

        resultdatetime = PythonTimeBuilder.build_datetime(1981, 4, 5, hours=23, minutes=21, seconds=28.512400, tzinfo=UTCOffset(name='-1', minutes=-60))
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='-1', minutes=-60)))

        resultdatetime = PythonTimeBuilder.build_datetime(1981, 4, 5, hours=23, minutes=21, seconds=28, microseconds=512400, tzinfo=UTCOffset(name='+1.5', minutes=90))
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='+1.5', minutes=90)))

    def test_build_timedelta(self):
        timedelta = PythonTimeBuilder.build_timedelta(years=1, months=2, days=3, weeks=4, hours=5, minutes=6, seconds=7, milliseconds=8, microseconds=9.1011)
        self.assertEqual(timedelta, datetime.timedelta(days=428, seconds=7, microseconds=9.1011, milliseconds=8, minutes=6, hours=5, weeks=4))

        timedelta = PythonTimeBuilder.build_timedelta(years=1, months=-2, days=3, weeks=-4, hours=5, minutes=-6, seconds=7, milliseconds=-8, microseconds=9.1011)
        self.assertEqual(timedelta, datetime.timedelta(days=308, seconds=7, microseconds=9.1011, milliseconds=-8, minutes=-6, hours=5, weeks=-4))

    def test_build_combine(self):
        date = PythonTimeBuilder.build_date(1, 2, 3)
        time = PythonTimeBuilder.build_time(hours=23, minutes=21, seconds=28, microseconds=512400)

        self.assertEqual(PythonTimeBuilder.combine(date, time), datetime.datetime(1, 2, 3, hour=23, minute=21, second=28, microsecond=512400))

class TestRelativeTimeBuilder(unittest.TestCase):
    def test_build_date(self):
        self.assertEqual(RelativeTimeBuilder.build_date(1, 2, 3), datetime.date(1, 2, 3))

    def test_build_time(self):
        time = RelativeTimeBuilder.build_time()
        self.assertEqual(time, datetime.time())

        time = RelativeTimeBuilder.build_time(hours=1, minutes=23)
        self.assertEqual(time, datetime.time(hour=1, minute=23))

        time = RelativeTimeBuilder.build_time(hours=1, minutes=23.4567)
        self.assertEqual(time, datetime.time(hour=1, minute=23, second=27, microsecond=402000))

        time = RelativeTimeBuilder.build_time(hours=23, minutes=21, seconds=28.512400)
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400))

        time = RelativeTimeBuilder.build_time(hours=23, minutes=21, seconds=28, microseconds=512400)
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400))

        time = RelativeTimeBuilder.build_time(tzinfo=UTCOffset(name='UTC', minutes=0))
        self.assertEqual(time, datetime.time(tzinfo=UTCOffset(name='UTC', minutes=0)))

        time = RelativeTimeBuilder.build_time(hours=1, minutes=23, tzinfo=UTCOffset(name='+1', minutes=60))
        self.assertEqual(time, datetime.time(hour=1, minute=23, tzinfo=UTCOffset(name='+1', minutes=60)))

        time = RelativeTimeBuilder.build_time(hours=1, minutes=23.4567, tzinfo=UTCOffset(name='-1', minutes=-60))
        self.assertEqual(time, datetime.time(hour=1, minute=23, second=27, microsecond=402000, tzinfo=UTCOffset(name='-1', minutes=-60)))

        time = RelativeTimeBuilder.build_time(hours=23, minutes=21, seconds=28.512400, tzinfo=UTCOffset(name='+1.5', minutes=90))
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='+1.5', minutes=90)))

        time = RelativeTimeBuilder.build_time(hours=23, minutes=21, seconds=28, microseconds=512400, tzinfo=UTCOffset(name='-1.5', minutes=-90))
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='-1.5', minutes=-90)))

    def test_build_datetime(self):
        resultdatetime = RelativeTimeBuilder.build_datetime(1981, 4, 5)
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5))

        resultdatetime = RelativeTimeBuilder.build_datetime(1981, 4, 5, hours=1, minutes=23.4567)
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=1, minute=23, second=27, microsecond=402000))

        resultdatetime = RelativeTimeBuilder.build_datetime(1981, 4, 5, hours=23, minutes=21, seconds=28.512400)
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=23, minute=21, second=28, microsecond=512400))

        resultdatetime = RelativeTimeBuilder.build_datetime(1981, 4, 5, hours=23, minutes=21, seconds=28, microseconds=512400)
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=23, minute=21, second=28, microsecond=512400))

        resultdatetime = RelativeTimeBuilder.build_datetime(1981, 4, 5, tzinfo=UTCOffset(name='UTC', minutes=0))
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, tzinfo=UTCOffset(name='UTC', minutes=0)))

        resultdatetime = RelativeTimeBuilder.build_datetime(1981, 4, 5, hours=1, minutes=23.4567, tzinfo=UTCOffset(name='+1', minutes=60))
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=1, minute=23, second=27, microsecond=402000, tzinfo=UTCOffset(name='+1', minutes=60)))

        resultdatetime = RelativeTimeBuilder.build_datetime(1981, 4, 5, hours=23, minutes=21, seconds=28.512400, tzinfo=UTCOffset(name='-1', minutes=-60))
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='-1', minutes=-60)))

        resultdatetime = RelativeTimeBuilder.build_datetime(1981, 4, 5, hours=23, minutes=21, seconds=28, microseconds=512400, tzinfo=UTCOffset(name='+1.5', minutes=90))
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='+1.5', minutes=90)))

    def test_build_timedelta(self):
        timedelta = RelativeTimeBuilder.build_timedelta(years=1, months=2, days=3, weeks=4, hours=5, minutes=6, seconds=7, milliseconds=8, microseconds=9.1011)
        self.assertEqual(timedelta, dateutil.relativedelta.relativedelta(years=1, months=2, days=31, hours=5, minutes=6, seconds=7.008, microseconds=9.1011))

        timedelta = RelativeTimeBuilder.build_timedelta(years=1, months=-2, days=3, weeks=-4, hours=5, minutes=-6, seconds=7, milliseconds=-8, microseconds=9.1011)
        self.assertEqual(timedelta, dateutil.relativedelta.relativedelta(years=1, months=-2, days=-25, hours=5, minutes=-6, seconds=6.992, microseconds=9.1011))

    def test_build_timedelta_nodateutil(self):
        import sys
        import dateutil

        dateutil_import = dateutil

        sys.modules['dateutil'] = None

        with self.assertRaises(RuntimeError):
            RelativeTimeBuilder.build_timedelta(years=1, months=2, days=3, weeks=4, hours=5, minutes=6, seconds=7, milliseconds=8, microseconds=9.1011)

        #Reinstall dateutil
        sys.modules['dateutil'] = dateutil

    def test_build_combine(self):
        date = RelativeTimeBuilder.build_date(1, 2, 3)
        time = RelativeTimeBuilder.build_time(hours=23, minutes=21, seconds=28, microseconds=512400)

        self.assertEqual(RelativeTimeBuilder.combine(date, time), datetime.datetime(1, 2, 3, hour=23, minute=21, second=28, microsecond=512400))
