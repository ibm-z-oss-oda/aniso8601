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
from aniso8601.exceptions import DayOutOfBoundsError, WeekOutOfBoundsError, \
        YearOutOfBoundsError
from aniso8601.timezone import UTCOffset

class TestBaseTimeBuilder(unittest.TestCase):
    def test_build_date(self):
        with self.assertRaises(NotImplementedError):
            BaseTimeBuilder.build_date()

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
        date = PythonTimeBuilder.build_date(YYYY='2013', MM=None, DD=None, Www=None, D=None, DDD=None)
        self.assertEqual(date, datetime.date(2013, 1, 1))

        date = PythonTimeBuilder.build_date(YYYY='0001', MM=None, DD=None, Www=None, D=None, DDD=None)
        self.assertEqual(date, datetime.date(1, 1, 1))

        date = PythonTimeBuilder.build_date(YYYY='1900', MM=None, DD=None, Www=None, D=None, DDD=None)
        self.assertEqual(date, datetime.date(1900, 1, 1))

        date = PythonTimeBuilder.build_date(YYYY='1981', MM='04', DD='05', Www=None, D=None, DDD=None)
        self.assertEqual(date, datetime.date(1981, 4, 5))

        date = PythonTimeBuilder.build_date(YYYY='1981', MM='04', DD=None, Www=None, D=None, DDD=None)
        self.assertEqual(date, datetime.date(1981, 4, 1))

        date = PythonTimeBuilder.build_date(YYYY='2004', MM=None, DD=None, Www='53', D=None, DDD=None)
        self.assertEqual(date, datetime.date(2004, 12, 27))
        self.assertEqual(date.weekday(), 0)

        date = PythonTimeBuilder.build_date(YYYY='2009', MM=None, DD=None, Www='01', D=None, DDD=None)
        self.assertEqual(date, datetime.date(2008, 12, 29))
        self.assertEqual(date.weekday(), 0)

        date = PythonTimeBuilder.build_date(YYYY='2010', MM=None, DD=None, Www='01', D=None, DDD=None)
        self.assertEqual(date, datetime.date(2010, 1, 4))
        self.assertEqual(date.weekday(), 0)

        date = PythonTimeBuilder.build_date(YYYY='2009', MM=None, DD=None, Www='53', D=None, DDD=None)
        self.assertEqual(date, datetime.date(2009, 12, 28))
        self.assertEqual(date.weekday(), 0)

        date = PythonTimeBuilder.build_date(YYYY='2009', MM=None, DD=None, Www='01', D='1', DDD=None)
        self.assertEqual(date, datetime.date(2008, 12, 29))
        self.assertEqual(date.weekday(), 0)

        date = PythonTimeBuilder.build_date(YYYY='2009', MM=None, DD=None, Www='53', D='7', DDD=None)
        self.assertEqual(date, datetime.date(2010, 1, 3))
        self.assertEqual(date.weekday(), 6)

        date = PythonTimeBuilder.build_date(YYYY='2010', MM=None, DD=None, Www='01', D='1', DDD=None)
        self.assertEqual(date, datetime.date(2010, 1, 4))
        self.assertEqual(date.weekday(), 0)

        date = PythonTimeBuilder.build_date(YYYY='2004', MM=None, DD=None, Www='53', D='6', DDD=None)
        self.assertEqual(date, datetime.date(2005, 1, 1))
        self.assertEqual(date.weekday(), 5)

        date = PythonTimeBuilder.build_date(YYYY='1981', MM=None, DD=None, Www=None, D=None, DDD='095')
        self.assertEqual(date, datetime.date(1981, 4, 5))

        date = PythonTimeBuilder.build_date(YYYY='1981', MM=None, DD=None, Www=None, D=None, DDD='365')
        self.assertEqual(date, datetime.date(1981, 12, 31))

        date = PythonTimeBuilder.build_date(YYYY='1980', MM=None, DD=None, Www=None, D=None, DDD='366')
        self.assertEqual(date, datetime.date(1980, 12, 31))

    def test_build_date_bounds_checking(self):
        #0 isn't a valid week number
        with self.assertRaises(WeekOutOfBoundsError):
            PythonTimeBuilder.build_date(YYYY='2003', Www='00')

        #Week must not be larger than 53
        with self.assertRaises(WeekOutOfBoundsError):
            PythonTimeBuilder.build_date(YYYY='2004', Www='54')

        #0 isn't a valid day number
        with self.assertRaises(DayOutOfBoundsError):
            PythonTimeBuilder.build_date(YYYY='2001', Www='02', D='0')

        #Day must not be larger than 7
        with self.assertRaises(DayOutOfBoundsError):
            PythonTimeBuilder.build_date(YYYY='2001', Www='02', D='8')

        #0 isn't a valid year for a Python builder
        with self.assertRaises(YearOutOfBoundsError):
            PythonTimeBuilder.build_date(YYYY='0000')

        with self.assertRaises(DayOutOfBoundsError):
            PythonTimeBuilder.build_date(YYYY='1981', DDD='000')

        #Day 366 is only valid on a leap year
        with self.assertRaises(DayOutOfBoundsError):
            PythonTimeBuilder.build_date(YYYY='1981', DDD='366')

        #Day must me 365, or 366, not larger
        with self.assertRaises(DayOutOfBoundsError):
            PythonTimeBuilder.build_date(YYYY='1981', DDD='367')

    def test_build_time(self):
        time = PythonTimeBuilder.build_time()
        self.assertEqual(time, datetime.time())

        time = PythonTimeBuilder.build_time(hours=1, minutes=23)
        self.assertEqual(time, datetime.time(hour=1, minute=23))

        time = PythonTimeBuilder.build_time(hours=1, minutes='23.4567')
        self.assertEqual(time, datetime.time(hour=1, minute=23, second=27, microsecond=402000))

        time = PythonTimeBuilder.build_time(hours=23, minutes=21, seconds='28.512400')
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400))

        time = PythonTimeBuilder.build_time(hours=23, minutes=21, seconds=28, microseconds=512400)
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400))

        time = PythonTimeBuilder.build_time(tzinfo=UTCOffset(name='UTC', minutes=0))
        self.assertEqual(time, datetime.time(tzinfo=UTCOffset(name='UTC', minutes=0)))

        time = PythonTimeBuilder.build_time(hours=1, minutes=23, tzinfo=UTCOffset(name='+1', minutes=60))
        self.assertEqual(time, datetime.time(hour=1, minute=23, tzinfo=UTCOffset(name='+1', minutes=60)))

        time = PythonTimeBuilder.build_time(hours=1, minutes='23.4567', tzinfo=UTCOffset(name='-1', minutes=-60))
        self.assertEqual(time, datetime.time(hour=1, minute=23, second=27, microsecond=402000, tzinfo=UTCOffset(name='-1', minutes=-60)))

        time = PythonTimeBuilder.build_time(hours=23, minutes=21, seconds='28.512400', tzinfo=UTCOffset(name='+1.5', minutes=90))
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='+1.5', minutes=90)))

        time = PythonTimeBuilder.build_time(hours=23, minutes=21, seconds=28, microseconds=512400, tzinfo=UTCOffset(name='-1.5', minutes=-90))
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='-1.5', minutes=-90)))

    def test_build_datetime(self):
        resultdatetime = PythonTimeBuilder.build_datetime(1981, 4, 5)
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5))

        resultdatetime = PythonTimeBuilder.build_datetime(1981, 4, 5, hours=1, minutes='23.4567')
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=1, minute=23, second=27, microsecond=402000))

        resultdatetime = PythonTimeBuilder.build_datetime(1981, 4, 5, hours=23, minutes=21, seconds='28.512400')
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=23, minute=21, second=28, microsecond=512400))

        resultdatetime = PythonTimeBuilder.build_datetime(1981, 4, 5, hours=23, minutes=21, seconds=28, microseconds=512400)
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=23, minute=21, second=28, microsecond=512400))

        resultdatetime = PythonTimeBuilder.build_datetime(1981, 4, 5, tzinfo=UTCOffset(name='UTC', minutes=0))
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, tzinfo=UTCOffset(name='UTC', minutes=0)))

        resultdatetime = PythonTimeBuilder.build_datetime(1981, 4, 5, hours=1, minutes='23.4567', tzinfo=UTCOffset(name='+1', minutes=60))
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=1, minute=23, second=27, microsecond=402000, tzinfo=UTCOffset(name='+1', minutes=60)))

        resultdatetime = PythonTimeBuilder.build_datetime(1981, 4, 5, hours=23, minutes=21, seconds='28.512400', tzinfo=UTCOffset(name='-1', minutes=-60))
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='-1', minutes=-60)))

        resultdatetime = PythonTimeBuilder.build_datetime(1981, 4, 5, hours=23, minutes=21, seconds=28, microseconds=512400, tzinfo=UTCOffset(name='+1.5', minutes=90))
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='+1.5', minutes=90)))

    def test_build_timedelta(self):
        timedelta = PythonTimeBuilder.build_timedelta(years=1, months=2, days=3, weeks=4, hours=5, minutes=6, seconds=7, microseconds=9.1011)
        self.assertEqual(timedelta, datetime.timedelta(days=428, seconds=7, microseconds=9.1011, minutes=6, hours=5, weeks=4))

        timedelta = PythonTimeBuilder.build_timedelta(years=1, months=-2, days=3, weeks=-4, hours=5, minutes=-6, seconds=7, microseconds=9.1011)
        self.assertEqual(timedelta, datetime.timedelta(days=308, seconds=7, microseconds=9.1011, minutes=-6, hours=5, weeks=-4))

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

        time = RelativeTimeBuilder.build_time(hours=1, minutes='23.4567')
        self.assertEqual(time, datetime.time(hour=1, minute=23, second=27, microsecond=402000))

        time = RelativeTimeBuilder.build_time(hours=23, minutes=21, seconds='28.512400')
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400))

        time = RelativeTimeBuilder.build_time(hours=23, minutes=21, seconds=28, microseconds=512400)
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400))

        time = RelativeTimeBuilder.build_time(tzinfo=UTCOffset(name='UTC', minutes=0))
        self.assertEqual(time, datetime.time(tzinfo=UTCOffset(name='UTC', minutes=0)))

        time = RelativeTimeBuilder.build_time(hours=1, minutes=23, tzinfo=UTCOffset(name='+1', minutes=60))
        self.assertEqual(time, datetime.time(hour=1, minute=23, tzinfo=UTCOffset(name='+1', minutes=60)))

        time = RelativeTimeBuilder.build_time(hours=1, minutes='23.4567', tzinfo=UTCOffset(name='-1', minutes=-60))
        self.assertEqual(time, datetime.time(hour=1, minute=23, second=27, microsecond=402000, tzinfo=UTCOffset(name='-1', minutes=-60)))

        time = RelativeTimeBuilder.build_time(hours=23, minutes=21, seconds='28.512400', tzinfo=UTCOffset(name='+1.5', minutes=90))
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='+1.5', minutes=90)))

        time = RelativeTimeBuilder.build_time(hours=23, minutes=21, seconds=28, microseconds=512400, tzinfo=UTCOffset(name='-1.5', minutes=-90))
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='-1.5', minutes=-90)))

    def test_build_datetime(self):
        resultdatetime = RelativeTimeBuilder.build_datetime(1981, 4, 5)
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5))

        resultdatetime = RelativeTimeBuilder.build_datetime(1981, 4, 5, hours=1, minutes='23.4567')
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=1, minute=23, second=27, microsecond=402000))

        resultdatetime = RelativeTimeBuilder.build_datetime(1981, 4, 5, hours=23, minutes=21, seconds='28.512400')
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=23, minute=21, second=28, microsecond=512400))

        resultdatetime = RelativeTimeBuilder.build_datetime(1981, 4, 5, hours=23, minutes=21, seconds=28, microseconds=512400)
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=23, minute=21, second=28, microsecond=512400))

        resultdatetime = RelativeTimeBuilder.build_datetime(1981, 4, 5, tzinfo=UTCOffset(name='UTC', minutes=0))
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, tzinfo=UTCOffset(name='UTC', minutes=0)))

        resultdatetime = RelativeTimeBuilder.build_datetime(1981, 4, 5, hours=1, minutes='23.4567', tzinfo=UTCOffset(name='+1', minutes=60))
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=1, minute=23, second=27, microsecond=402000, tzinfo=UTCOffset(name='+1', minutes=60)))

        resultdatetime = RelativeTimeBuilder.build_datetime(1981, 4, 5, hours=23, minutes=21, seconds='28.512400', tzinfo=UTCOffset(name='-1', minutes=-60))
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='-1', minutes=-60)))

        resultdatetime = RelativeTimeBuilder.build_datetime(1981, 4, 5, hours=23, minutes=21, seconds=28, microseconds=512400, tzinfo=UTCOffset(name='+1.5', minutes=90))
        self.assertEqual(resultdatetime, datetime.datetime(1981, 4, 5, hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='+1.5', minutes=90)))

    def test_build_timedelta(self):
        timedelta = RelativeTimeBuilder.build_timedelta(years=1, months=2, days=3, weeks=4, hours=5, minutes=6, seconds=7, microseconds='9.1011')
        self.assertEqual(timedelta, dateutil.relativedelta.relativedelta(years=1, months=2, days=31, hours=5, minutes=6, seconds=7, microseconds=9.1011))

        timedelta = RelativeTimeBuilder.build_timedelta(years=1, months=-2, days=3, weeks=-4, hours=5, minutes=-6, seconds=7, microseconds='9.1011')
        self.assertEqual(timedelta, dateutil.relativedelta.relativedelta(years=1, months=-2, days=-25, hours=5, minutes=-6, seconds=7, microseconds=9.1011))

    def test_build_timedelta_nodateutil(self):
        import sys
        import dateutil

        dateutil_import = dateutil

        sys.modules['dateutil'] = None

        with self.assertRaises(RuntimeError):
            RelativeTimeBuilder.build_timedelta(years=1, months=2, days=3, weeks=4, hours=5, minutes=6, seconds=7, microseconds=9.1011)

        #Reinstall dateutil
        sys.modules['dateutil'] = dateutil

    def test_build_combine(self):
        date = RelativeTimeBuilder.build_date(1, 2, 3)
        time = RelativeTimeBuilder.build_time(hours=23, minutes=21, seconds=28, microseconds=512400)

        self.assertEqual(RelativeTimeBuilder.combine(date, time), datetime.datetime(1, 2, 3, hour=23, minute=21, second=28, microsecond=512400))
