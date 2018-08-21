# -*- coding: utf-8 -*-

# Copyright (c) 2016, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime
import pickle
import unittest
import dateutil.relativedelta

from aniso8601 import compat
from aniso8601.builder import BaseTimeBuilder, PythonTimeBuilder, RelativeTimeBuilder, UTCOffset
from aniso8601.exceptions import DayOutOfBoundsError, HoursOutOfBoundsError, \
        LeapSecondError, MidnightBoundsError, MinutesOutOfBoundsError, \
        SecondsOutOfBoundsError, WeekOutOfBoundsError, YearOutOfBoundsError

class TestBaseTimeBuilder(unittest.TestCase):
    def test_build_date(self):
        with self.assertRaises(NotImplementedError):
            BaseTimeBuilder.build_date()

    def test_build_time(self):
        with self.assertRaises(NotImplementedError):
            BaseTimeBuilder.build_time()

    def test_build_duration(self):
        with self.assertRaises(NotImplementedError):
            BaseTimeBuilder.build_duration()

    def test_build_timezone(self):
        with self.assertRaises(NotImplementedError):
            BaseTimeBuilder.build_timezone()

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

        time = PythonTimeBuilder.build_time(hh='1', mm='23')
        self.assertEqual(time, datetime.time(hour=1, minute=23))

        time = PythonTimeBuilder.build_time(hh='1', mm='23', ss='45')
        self.assertEqual(time, datetime.time(hour=1, minute=23, second=45))

        time = PythonTimeBuilder.build_time(hh='1', mm='23.4567')
        self.assertEqual(time, datetime.time(hour=1, minute=23, second=27, microsecond=402000))

        time = PythonTimeBuilder.build_time(hh='23', mm='21', ss='28.512400')
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400))

        time = PythonTimeBuilder.build_time(hh='14', mm='43', ss='59.9999997')
        self.assertEqual(time, datetime.time(hour=14, minute=43, second=59, microsecond=999999))

        time = PythonTimeBuilder.build_time(hh='12.5')
        self.assertEqual(time, datetime.time(hour=12, minute=30))

        time = PythonTimeBuilder.build_time(hh='24')
        self.assertEqual(time, datetime.time(hour=0))

        time = PythonTimeBuilder.build_time(hh='24', mm='00')
        self.assertEqual(time, datetime.time(hour=0))

        time = PythonTimeBuilder.build_time(hh='24', mm='00', ss='00')
        self.assertEqual(time, datetime.time(hour=0))

        time = PythonTimeBuilder.build_time(tz=(False, None, '00', '00', 'UTC', 'timezone'))
        self.assertEqual(time, datetime.time(tzinfo=UTCOffset(name='UTC', minutes=0)))

        time = PythonTimeBuilder.build_time(hh='23', mm='21', ss='28.512400', tz=(False, None, '00', '00', '+00:00', 'timezone'))
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='+00:00', minutes=0)))

        time = PythonTimeBuilder.build_time(hh='1', mm='23', tz=(False, None, '01', '00', '+1', 'timezone'))
        self.assertEqual(time, datetime.time(hour=1, minute=23, tzinfo=UTCOffset(name='+1', minutes=60)))

        time = PythonTimeBuilder.build_time(hh='1', mm='23.4567', tz=(True, None, '01', '00', '-1', 'timezone'))
        self.assertEqual(time, datetime.time(hour=1, minute=23, second=27, microsecond=402000, tzinfo=UTCOffset(name='-1', minutes=-60)))

        time = PythonTimeBuilder.build_time(hh='23', mm='21', ss='28.512400', tz=(False, None, '01', '30', '+1:30', 'timezone'))
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='+1:30', minutes=90)))

        time = PythonTimeBuilder.build_time(hh='23', mm='21', ss='28.512400', tz=(False, None, '11', '15', '+11:15', 'timezone'))
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='+11:15', minutes=675)))

        time = PythonTimeBuilder.build_time(hh='23', mm='21', ss='28.512400', tz=(False, None, '12', '34', '+12:34', 'timezone'))
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='+12:34', minutes=754)))

        time = PythonTimeBuilder.build_time(hh='23', mm='21', ss='28.512400', tz=(False, None, '00', '00', 'UTC', 'timezone'))
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='UTC', minutes=0)))

    def test_build_time_bounds_checking(self):
        #Leap seconds not supported
        #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
        #https://bitbucket.org/nielsenb/aniso8601/issues/13/parsing-of-leap-second-gives-wildly
        with self.assertRaises(LeapSecondError):
            PythonTimeBuilder.build_time(hh='23', mm='59', ss='60')

        with self.assertRaises(LeapSecondError):
            PythonTimeBuilder.build_time(hh='23', mm='59', ss='60', tz=UTCOffset(name='UTC', minutes=0))

        with self.assertRaises(SecondsOutOfBoundsError):
            PythonTimeBuilder.build_time(hh='00', mm='00', ss='60')

        with self.assertRaises(SecondsOutOfBoundsError):
            PythonTimeBuilder.build_time(hh='00', mm='00', ss='60', tz=UTCOffset(name='UTC', minutes=0))

        with self.assertRaises(SecondsOutOfBoundsError):
            PythonTimeBuilder.build_time(hh='00', mm='00', ss='61')

        with self.assertRaises(SecondsOutOfBoundsError):
            PythonTimeBuilder.build_time(hh='00', mm='00', ss='61', tz=UTCOffset(name='UTC', minutes=0))

        with self.assertRaises(MinutesOutOfBoundsError):
            PythonTimeBuilder.build_time(hh='00', mm='61')

        with self.assertRaises(MinutesOutOfBoundsError):
            PythonTimeBuilder.build_time(hh='00', mm='61', tz=UTCOffset(name='UTC', minutes=0))

        with self.assertRaises(MinutesOutOfBoundsError):
            PythonTimeBuilder.build_time(hh='00', mm='60')

        with self.assertRaises(MinutesOutOfBoundsError):
            PythonTimeBuilder.build_time(hh='00', mm='60.1')

        with self.assertRaises(HoursOutOfBoundsError):
            PythonTimeBuilder.build_time(hh='25')

        with self.assertRaises(HoursOutOfBoundsError):
            PythonTimeBuilder.build_time(hh='24.1')

        #Hour 24 can only represent midnight
        with self.assertRaises(MidnightBoundsError):
            PythonTimeBuilder.build_time(hh='24', mm='00', ss='01')

        with self.assertRaises(MidnightBoundsError):
            PythonTimeBuilder.build_time(hh='24', mm='00.1')

        with self.assertRaises(MidnightBoundsError):
            PythonTimeBuilder.build_time(hh='24', mm='01')

    def test_build_datetime(self):
        self.assertEqual(PythonTimeBuilder.build_datetime(('1', '2', '3', None, None, None, 'date'), ('23', '21', '28.512400', None, 'time')), datetime.datetime(1, 2, 3, hour=23, minute=21, second=28, microsecond=512400))

        self.assertEqual(PythonTimeBuilder.build_datetime(('1981', '04', '05', None, None, None, 'date'), ('23', '21', '28.512400', (False, None, '11', '15', '+11:15', 'timezone'), 'time')), datetime.datetime(1981, 4, 5, hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='+11:15', minutes=675)))

    def test_build_datetime_bounds_checking(self):
        #Leap seconds not supported
        #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
        #https://bitbucket.org/nielsenb/aniso8601/issues/13/parsing-of-leap-second-gives-wildly
        with self.assertRaises(LeapSecondError):
            PythonTimeBuilder.build_datetime(('2016', '12', '31', None, None, None, 'date'), ('23', '59', '60', None, 'time'))

        with self.assertRaises(LeapSecondError):
            PythonTimeBuilder.build_datetime(('2016', '12', '31', None, None, None, 'date'), ('23', '59', '60', (False, None, '00', '00', '+00:00', 'timezone'), 'time'))

        with self.assertRaises(SecondsOutOfBoundsError):
            PythonTimeBuilder.build_datetime(('1981', '04', '05', None, None, None, 'date'), ('00', '00', '60', None, 'time'))

        with self.assertRaises(SecondsOutOfBoundsError):
            PythonTimeBuilder.build_datetime(('1981', '04', '05', None, None, None, 'date'), ('00', '00', '60', (False, None, '00', '00', '+00:00', 'timezone'), 'time'))

        with self.assertRaises(SecondsOutOfBoundsError):
            PythonTimeBuilder.build_datetime(('1981', '04', '05', None, None, None, 'date'), ('00', '00', '61', None, 'time'))

        with self.assertRaises(SecondsOutOfBoundsError):
            PythonTimeBuilder.build_datetime(('1981', '04', '05', None, None, None, 'date'), ('00', '00', '61', (False, None, '00', '00', '+00:00', 'timezone'), 'time'))

        with self.assertRaises(SecondsOutOfBoundsError):
            PythonTimeBuilder.build_datetime(('1981', '04', '05', None, None, None, 'date'), ('00', '59', '61', None, 'time'))

        with self.assertRaises(SecondsOutOfBoundsError):
            PythonTimeBuilder.build_datetime(('1981', '04', '05', None, None, None, 'date'), ('00', '59', '61', (False, None, '00', '00', '+00:00', 'timezone'), 'time'))

        with self.assertRaises(MinutesOutOfBoundsError):
            PythonTimeBuilder.build_datetime(('1981', '04', '05', None, None, None, 'date'), ('00', '61', None, None, 'time'))

        with self.assertRaises(MinutesOutOfBoundsError):
            PythonTimeBuilder.build_datetime(('1981', '04', '05', None, None, None, 'date'), ('00', '61', None, (False, None, '00', '00', '+00:00', 'timezone'), 'time'))

    def test_build_duration(self):
        timedelta = PythonTimeBuilder.build_duration(PnY='1', PnM='2', PnD='3', TnH='4', TnM='54', TnS='6')
        self.assertEqual(timedelta, datetime.timedelta(days=428, seconds=17646))

        timedelta = PythonTimeBuilder.build_duration(PnY='1', PnM='2', PnD='3', TnH='4', TnM='54', TnS='6.5')
        self.assertEqual(timedelta, datetime.timedelta(days=428, seconds=17646.5))

        timedelta = PythonTimeBuilder.build_duration(PnY='1', PnM='2', PnD='3', TnH='4', TnM='54', TnS='6')
        self.assertEqual(timedelta, datetime.timedelta(days=428, hours=4, minutes=54, seconds=6))

        timedelta = PythonTimeBuilder.build_duration(PnY='1', PnM='2', PnD='3', TnH='4', TnM='54', TnS='6.5')
        self.assertEqual(timedelta, datetime.timedelta(days=428, hours=4, minutes=54, seconds=6.5))

        timedelta = PythonTimeBuilder.build_duration(PnY='1', PnM='2', PnD='3')
        self.assertEqual(timedelta, datetime.timedelta(days=428))

        timedelta = PythonTimeBuilder.build_duration(PnY='1', PnM='2', PnD='3.5')
        self.assertEqual(timedelta, datetime.timedelta(days=428.5))

        timedelta = PythonTimeBuilder.build_duration(TnH='4', TnM='54', TnS='6.5')
        self.assertEqual(timedelta, datetime.timedelta(hours=4, minutes=54, seconds=6.5))

        #Make sure we truncate, not round
        #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
        timedelta = PythonTimeBuilder.build_duration(TnS='0.0000001')
        self.assertEqual(timedelta, datetime.timedelta(0))

        timedelta = PythonTimeBuilder.build_duration(TnS='2.0000048')
        self.assertEqual(timedelta, datetime.timedelta(seconds=2, microseconds=4))

        timedelta = PythonTimeBuilder.build_duration(PnY='1')
        self.assertEqual(timedelta, datetime.timedelta(days=365))

        timedelta = PythonTimeBuilder.build_duration(PnY='1.5')
        self.assertEqual(timedelta, datetime.timedelta(days=547.5))

        timedelta = PythonTimeBuilder.build_duration(PnM='1')
        self.assertEqual(timedelta, datetime.timedelta(days=30))

        timedelta = PythonTimeBuilder.build_duration(PnM='1.5')
        self.assertEqual(timedelta, datetime.timedelta(days=45))

        timedelta = PythonTimeBuilder.build_duration(PnW='1')
        self.assertEqual(timedelta, datetime.timedelta(days=7))

        timedelta = PythonTimeBuilder.build_duration(PnW='1.5')
        self.assertEqual(timedelta, datetime.timedelta(days=10.5))

        timedelta = PythonTimeBuilder.build_duration(PnD='1')
        self.assertEqual(timedelta, datetime.timedelta(days=1))

        timedelta = PythonTimeBuilder.build_duration(PnD='1.5')
        self.assertEqual(timedelta, datetime.timedelta(days=1.5))

        timedelta = PythonTimeBuilder.build_duration(PnY='0003', PnM='06', PnD='04', TnH='12', TnM='30', TnS='05')
        self.assertEqual(timedelta, datetime.timedelta(days=1279, hours=12, minutes=30, seconds=5))

        timedelta = PythonTimeBuilder.build_duration(PnY='0003', PnM='06', PnD='04', TnH='12', TnM='30', TnS='05.5')
        self.assertEqual(timedelta, datetime.timedelta(days=1279, hours=12, minutes=30, seconds=5.5))

        timedelta = PythonTimeBuilder.build_duration(PnY='0003', PnM='06', PnD='04', TnH='12', TnM='30', TnS='05')
        self.assertEqual(timedelta, datetime.timedelta(days=1279, hours=12, minutes=30, seconds=5))

        timedelta = PythonTimeBuilder.build_duration(PnY='0003', PnM='06', PnD='04', TnH='12', TnM='30', TnS='05.5')
        self.assertEqual(timedelta, datetime.timedelta(days=1279, hours=12, minutes=30, seconds=5.5))

        #Make sure we truncate, not round
        #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
        timedelta = PythonTimeBuilder.build_duration(PnY='0001', PnM='02', PnD='03', TnH='14', TnM='43', TnS='59.9999997')
        self.assertEqual(timedelta, datetime.timedelta(days=428, hours=14, minutes=43, seconds=59, microseconds=999999))

        #Verify overflows
        self.assertEqual(PythonTimeBuilder.build_duration(TnH='36'), PythonTimeBuilder.build_duration(PnD='1', TnH='12'))

    def test_build_interval(self):
        interval = PythonTimeBuilder.build_interval(end=(('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), duration=(None, '1', None, None, None, None, None, 'duration'))
        self.assertEqual(interval[0], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))
        self.assertEqual(interval[1], datetime.datetime(year=1981, month=3, day=6, hour=1, minute=1))

        interval = PythonTimeBuilder.build_interval(end=('1981', '04', '05', None, None, None, 'date'), duration=(None, '1', None, None, None, None, None, 'duration'))
        self.assertEqual(interval[0], datetime.date(year=1981, month=4, day=5))
        self.assertEqual(interval[1], datetime.date(year=1981, month=3, day=6))

        interval = PythonTimeBuilder.build_interval(end=('2018', '03', '06', None, None, None, 'date'), duration=('1.5', None, None, None, None, None, None, 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2018, month=3, day=6))
        self.assertEqual(interval[1], datetime.date(year=2016, month=9, day=5))

        interval = PythonTimeBuilder.build_interval(end=('2014', '11', '12', None, None, None, 'date'), duration=(None, None, None, None, '1', None, None, 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2014, month=11, day=12))
        self.assertEqual(interval[1], datetime.datetime(year=2014, month=11, day=11, hour=23))

        interval = PythonTimeBuilder.build_interval(end=('2014', '11', '12', None, None, None, 'date'), duration=(None, None, None, None, '4', '54', '6.5', 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2014, month=11, day=12))
        self.assertEqual(interval[1], datetime.datetime(year=2014, month=11, day=11, hour=19, minute=5, second=53, microsecond=500000))

        #Make sure we truncate, not round
        #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
        interval = PythonTimeBuilder.build_interval(end=('2018', '03', '06', None, None, None, 'date'), duration=(None, None, None, None, None, None, '0.0000001', 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2018, month=3, day=6))
        self.assertEqual(interval[1], datetime.datetime(year=2018, month=3, day=6))

        interval = PythonTimeBuilder.build_interval(end=('2018', '03', '06', None, None, None, 'date'), duration=(None, None, None, None, None, None, '2.0000048', 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2018, month=3, day=6))
        self.assertEqual(interval[1], datetime.datetime(year=2018, month=3, day=5, hour=23, minute=59, second=57, microsecond=999996))

        interval = PythonTimeBuilder.build_interval(start=(('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), duration=(None, '1', None, '1', None, '1', None, 'duration'))
        self.assertEqual(interval[0], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))
        self.assertEqual(interval[1], datetime.datetime(year=1981, month=5, day=6, hour=1, minute=2))

        interval = PythonTimeBuilder.build_interval(start=('1981', '04', '05', None, None, None, 'date'), duration=(None, '1', None, '1', None, None, None, 'duration'))
        self.assertEqual(interval[0], datetime.date(year=1981, month=4, day=5))
        self.assertEqual(interval[1], datetime.date(year=1981, month=5, day=6))

        interval = PythonTimeBuilder.build_interval(start=('2018', '03', '06', None, None, None, 'date'), duration=(None, '2.5', None, None, None, None, None, 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2018, month=3, day=6))
        self.assertEqual(interval[1], datetime.date(year=2018, month=5, day=20))

        interval = PythonTimeBuilder.build_interval(start=('2014', '11', '12', None, None, None, 'date'), duration=(None, None, None, None, '1', None, None, 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2014, month=11, day=12))
        self.assertEqual(interval[1], datetime.datetime(year=2014, month=11, day=12, hour=1, minute=0))

        interval = PythonTimeBuilder.build_interval(start=('2014', '11', '12', None, None, None, 'date'), duration=(None, None, None, None, '4', '54', '6.5', 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2014, month=11, day=12))
        self.assertEqual(interval[1], datetime.datetime(year=2014, month=11, day=12, hour=4, minute=54, second=6, microsecond=500000))

        #Make sure we truncate, not round
        #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
        interval = PythonTimeBuilder.build_interval(start=('2018', '03', '06', None, None, None, 'date'), duration=(None, None, None, None, None, None, '0.0000001', 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2018, month=3, day=6))
        self.assertEqual(interval[1], datetime.datetime(year=2018, month=3, day=6))

        interval = PythonTimeBuilder.build_interval(start=('2018', '03', '06', None, None, None, 'date'), duration=(None, None, None, None, None, None, '2.0000048', 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2018, month=3, day=6))
        self.assertEqual(interval[1], datetime.datetime(year=2018, month=3, day=6, hour=0, minute=0, second=2, microsecond=4))

        interval = PythonTimeBuilder.build_interval(start=(('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), end=(('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'))
        self.assertEqual(interval[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(interval[1], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))

        interval = PythonTimeBuilder.build_interval(start=(('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), end=('1981', '04', '05', None, None, None, 'date'))
        self.assertEqual(interval[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(interval[1], datetime.date(year=1981, month=4, day=5))

        interval = PythonTimeBuilder.build_interval(start=('1980', '03', '05', None, None, None, 'date'), end=(('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'))
        self.assertEqual(interval[0], datetime.date(year=1980, month=3, day=5))
        self.assertEqual(interval[1], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))

        interval = PythonTimeBuilder.build_interval(start=('1980', '03', '05', None, None, None, 'date'), end=('1981', '04', '05', None, None, None, 'date'))
        self.assertEqual(interval[0], datetime.date(year=1980, month=3, day=5))
        self.assertEqual(interval[1], datetime.date(year=1981, month=4, day=5))

        interval = PythonTimeBuilder.build_interval(start=('1981', '04', '05', None, None, None, 'date'), end=('1980', '03', '05', None, None, None, 'date'))
        self.assertEqual(interval[0], datetime.date(year=1981, month=4, day=5))
        self.assertEqual(interval[1], datetime.date(year=1980, month=3, day=5))

        #Make sure we truncate, not round
        #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
        interval = PythonTimeBuilder.build_interval(start=(('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00.0000001', None, 'time'), 'datetime'), end=(('1981', '04', '05', None, None, None, 'date'), ('14', '43', '59.9999997', None, 'time'), 'datetime'))
        self.assertEqual(interval[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(interval[1], datetime.datetime(year=1981, month=4, day=5, hour=14, minute=43, second=59, microsecond=999999))

    def test_build_repeating_interval(self):
        results = list(PythonTimeBuilder.build_repeating_interval(Rnn='3', interval=(('1981', '04', '05', None, None, None, 'date'), None, (None, None, None, '1', None, None, None, 'duration'), 'interval')))
        self.assertEqual(results[0], datetime.date(year=1981, month=4, day=5))
        self.assertEqual(results[1], datetime.date(year=1981, month=4, day=6))
        self.assertEqual(results[2], datetime.date(year=1981, month=4, day=7))

        results = list(PythonTimeBuilder.build_repeating_interval(Rnn='11', interval=(None, (('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (None, None, None, None, '1', '2', None, 'duration'), 'interval')))

        for dateindex in compat.range(0, 11):
             self.assertEqual(results[dateindex], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1) - dateindex * datetime.timedelta(hours=1, minutes=2))

        results = list(PythonTimeBuilder.build_repeating_interval(Rnn='2', interval=((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, 'interval')))
        self.assertEqual(results[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(results[1], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))

        results = list(PythonTimeBuilder.build_repeating_interval(Rnn='2', interval=((('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), None, 'interval')))
        self.assertEqual(results[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(results[1], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))

        resultgenerator = PythonTimeBuilder.build_repeating_interval(R=True, interval=(None, (('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (None, None, None, None, '1', '2', None, 'duration'), 'interval'))

        #Tets the first 11 generated
        for dateindex in compat.range(0, 11):
             self.assertEqual(next(resultgenerator), datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1) - dateindex * datetime.timedelta(hours=1, minutes=2))

    def test_build_timezone(self):
        tzinfoobject = PythonTimeBuilder.build_timezone(Z=True, name='Z')
        self.assertEqual(tzinfoobject.utcoffset(None), datetime.timedelta(hours=0))
        self.assertEqual(tzinfoobject.tzname(None), 'UTC')

        tzinfoobject = PythonTimeBuilder.build_timezone(negative=False, hh='00', mm='00', name='+00:00')
        self.assertEqual(tzinfoobject.utcoffset(None), datetime.timedelta(hours=0))
        self.assertEqual(tzinfoobject.tzname(None), '+00:00')

        tzinfoobject = PythonTimeBuilder.build_timezone(negative=False, hh='01', mm='00', name='+01:00')
        self.assertEqual(tzinfoobject.utcoffset(None), datetime.timedelta(hours=1))
        self.assertEqual(tzinfoobject.tzname(None), '+01:00')

        tzinfoobject = PythonTimeBuilder.build_timezone(negative=True, hh='01', mm='00', name='-01:00')
        self.assertEqual(tzinfoobject.utcoffset(None), -datetime.timedelta(hours=1))
        self.assertEqual(tzinfoobject.tzname(None), '-01:00')

        tzinfoobject = PythonTimeBuilder.build_timezone(negative=False, hh='00', mm='12', name='+00:12')
        self.assertEqual(tzinfoobject.utcoffset(None), datetime.timedelta(minutes=12))
        self.assertEqual(tzinfoobject.tzname(None), '+00:12')

        tzinfoobject = PythonTimeBuilder.build_timezone(negative=False, hh='01', mm='23', name='+01:23')
        self.assertEqual(tzinfoobject.utcoffset(None), datetime.timedelta(hours=1, minutes=23))
        self.assertEqual(tzinfoobject.tzname(None), '+01:23')

        tzinfoobject = PythonTimeBuilder.build_timezone(negative=True, hh='01', mm='23', name='-01:23')
        self.assertEqual(tzinfoobject.utcoffset(None), -datetime.timedelta(hours=1, minutes=23))
        self.assertEqual(tzinfoobject.tzname(None), '-01:23')

        tzinfoobject = PythonTimeBuilder.build_timezone(negative=False, hh='00', name='+00')
        self.assertEqual(tzinfoobject.utcoffset(None), datetime.timedelta(hours=0))
        self.assertEqual(tzinfoobject.tzname(None), '+00')

        tzinfoobject = PythonTimeBuilder.build_timezone(negative=False, hh='01', name='+01')
        self.assertEqual(tzinfoobject.utcoffset(None), datetime.timedelta(hours=1))
        self.assertEqual(tzinfoobject.tzname(None), '+01')

        tzinfoobject = PythonTimeBuilder.build_timezone(negative=True, hh='01', name='-01')
        self.assertEqual(tzinfoobject.utcoffset(None), -datetime.timedelta(hours=1))
        self.assertEqual(tzinfoobject.tzname(None), '-01')

        tzinfoobject = PythonTimeBuilder.build_timezone(negative=False, hh='12', name='+12')
        self.assertEqual(tzinfoobject.utcoffset(None), datetime.timedelta(hours=12))
        self.assertEqual(tzinfoobject.tzname(None), '+12')

        tzinfoobject = PythonTimeBuilder.build_timezone(negative=True, hh='12', name='-12')
        self.assertEqual(tzinfoobject.utcoffset(None), -datetime.timedelta(hours=12))
        self.assertEqual(tzinfoobject.tzname(None), '-12')

class TestRelativeTimeBuilder(unittest.TestCase):
    def test_build_date(self):
        self.assertEqual(RelativeTimeBuilder.build_date(1, 2, 3), datetime.date(1, 2, 3))

    def test_build_time(self):
        time = RelativeTimeBuilder.build_time()
        self.assertEqual(time, datetime.time())

        time = RelativeTimeBuilder.build_time(hh='1', mm='23')
        self.assertEqual(time, datetime.time(hour=1, minute=23))

        time = RelativeTimeBuilder.build_time(hh='1', mm='23', ss='45')
        self.assertEqual(time, datetime.time(hour=1, minute=23, second=45))

        time = RelativeTimeBuilder.build_time(hh='1', mm='23.4567')
        self.assertEqual(time, datetime.time(hour=1, minute=23, second=27, microsecond=402000))

        time = RelativeTimeBuilder.build_time(hh='23', mm='21', ss='28.512400')
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400))

        time = RelativeTimeBuilder.build_time(hh='14', mm='43', ss='59.9999997')
        self.assertEqual(time, datetime.time(hour=14, minute=43, second=59, microsecond=999999))

        time = RelativeTimeBuilder.build_time(hh='12.5')
        self.assertEqual(time, datetime.time(hour=12, minute=30))

        time = RelativeTimeBuilder.build_time(hh='24')
        self.assertEqual(time, datetime.time(hour=0))

        time = RelativeTimeBuilder.build_time(hh='24', mm='00')
        self.assertEqual(time, datetime.time(hour=0))

        time = RelativeTimeBuilder.build_time(hh='24', mm='00', ss='00')
        self.assertEqual(time, datetime.time(hour=0))

        time = RelativeTimeBuilder.build_time(tz=UTCOffset(name='UTC', minutes=0))
        self.assertEqual(time, datetime.time(tzinfo=UTCOffset(name='UTC', minutes=0)))

        time = RelativeTimeBuilder.build_time(hh='23', mm='21', ss='28.512400', tz=UTCOffset(name='+00:00', minutes=0))
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='+00:00', minutes=0)))

        time = RelativeTimeBuilder.build_time(hh='1', mm='23', tz=UTCOffset(name='+1', minutes=60))
        self.assertEqual(time, datetime.time(hour=1, minute=23, tzinfo=UTCOffset(name='+1', minutes=60)))

        time = RelativeTimeBuilder.build_time(hh='1', mm='23.4567', tz=UTCOffset(name='-1', minutes=-60))
        self.assertEqual(time, datetime.time(hour=1, minute=23, second=27, microsecond=402000, tzinfo=UTCOffset(name='-1', minutes=-60)))

        time = RelativeTimeBuilder.build_time(hh='23', mm='21', ss='28.512400', tz=UTCOffset(name='+1.5', minutes=90))
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='+1.5', minutes=90)))

        time = RelativeTimeBuilder.build_time(hh='23', mm='21', ss='28.512400', tz=UTCOffset(name='+11:15', minutes=675))
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='+11:5', minutes=675)))

        time = RelativeTimeBuilder.build_time(hh='23', mm='21', ss='28.512400', tz=UTCOffset(name='-12:34', minutes=754))
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='+11.5', minutes=754)))

        time = RelativeTimeBuilder.build_time(hh='23', mm='21', ss='28.512400', tz=UTCOffset(name='UTC', minutes=0))
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='UTC', minutes=0)))

    def test_build_timezone(self):
        tzinfoobject = RelativeTimeBuilder.build_timezone(Z=True, name='Z')
        self.assertEqual(tzinfoobject.utcoffset(None), datetime.timedelta(hours=0))
        self.assertEqual(tzinfoobject.tzname(None), 'UTC')

        tzinfoobject = RelativeTimeBuilder.build_timezone(negative=False, hh='00', mm='00', name='+00:00')
        self.assertEqual(tzinfoobject.utcoffset(None), datetime.timedelta(hours=0))
        self.assertEqual(tzinfoobject.tzname(None), '+00:00')

        tzinfoobject = RelativeTimeBuilder.build_timezone(negative=False, hh='01', mm='00', name='+01:00')
        self.assertEqual(tzinfoobject.utcoffset(None), datetime.timedelta(hours=1))
        self.assertEqual(tzinfoobject.tzname(None), '+01:00')

        tzinfoobject = RelativeTimeBuilder.build_timezone(negative=True, hh='01', mm='00', name='-01:00')
        self.assertEqual(tzinfoobject.utcoffset(None), -datetime.timedelta(hours=1))
        self.assertEqual(tzinfoobject.tzname(None), '-01:00')

        tzinfoobject = RelativeTimeBuilder.build_timezone(negative=False, hh='00', mm='12', name='+00:12')
        self.assertEqual(tzinfoobject.utcoffset(None), datetime.timedelta(minutes=12))
        self.assertEqual(tzinfoobject.tzname(None), '+00:12')

        tzinfoobject = RelativeTimeBuilder.build_timezone(negative=False, hh='01', mm='23', name='+01:23')
        self.assertEqual(tzinfoobject.utcoffset(None), datetime.timedelta(hours=1, minutes=23))
        self.assertEqual(tzinfoobject.tzname(None), '+01:23')

        tzinfoobject = RelativeTimeBuilder.build_timezone(negative=True, hh='01', mm='23', name='-01:23')
        self.assertEqual(tzinfoobject.utcoffset(None), -datetime.timedelta(hours=1, minutes=23))
        self.assertEqual(tzinfoobject.tzname(None), '-01:23')

        tzinfoobject = RelativeTimeBuilder.build_timezone(negative=False, hh='00', name='+00')
        self.assertEqual(tzinfoobject.utcoffset(None), datetime.timedelta(hours=0))
        self.assertEqual(tzinfoobject.tzname(None), '+00')

        tzinfoobject = RelativeTimeBuilder.build_timezone(negative=False, hh='01', name='+01')
        self.assertEqual(tzinfoobject.utcoffset(None), datetime.timedelta(hours=1))
        self.assertEqual(tzinfoobject.tzname(None), '+01')

        tzinfoobject = RelativeTimeBuilder.build_timezone(negative=True, hh='01', name='-01')
        self.assertEqual(tzinfoobject.utcoffset(None), -datetime.timedelta(hours=1))
        self.assertEqual(tzinfoobject.tzname(None), '-01')

        tzinfoobject = RelativeTimeBuilder.build_timezone(negative=False, hh='12', name='+12')
        self.assertEqual(tzinfoobject.utcoffset(None), datetime.timedelta(hours=12))
        self.assertEqual(tzinfoobject.tzname(None), '+12')

        tzinfoobject = RelativeTimeBuilder.build_timezone(negative=True, hh='12', name='-12')
        self.assertEqual(tzinfoobject.utcoffset(None), -datetime.timedelta(hours=12))
        self.assertEqual(tzinfoobject.tzname(None), '-12')

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
        date = datetime.date(1, 2, 3)
        time = datetime.time(hour=23, minute=21, second=28, microsecond=512400)

        self.assertEqual(RelativeTimeBuilder.combine(date, time), datetime.datetime(1, 2, 3, hour=23, minute=21, second=28, microsecond=512400))

class TestUTCOffset(unittest.TestCase):
    def test_pickle(self):
        #Make sure timezone objects are pickleable
        testutcoffset = UTCOffset(name='UTC', minutes=0)

        utcoffsetpickle = pickle.dumps(testutcoffset)

        resultutcoffset = pickle.loads(utcoffsetpickle)

        self.assertEqual(resultutcoffset._name, testutcoffset._name)
        self.assertEqual(resultutcoffset._utcdelta, testutcoffset._utcdelta)

    def test_repr(self):
        self.assertEqual(str(UTCOffset(minutes=0)), '+0:00:00 UTC')

        self.assertEqual(str(UTCOffset(minutes=60)), '+1:00:00 UTC')

        self.assertEqual(str(UTCOffset(minutes=-60)), '-1:00:00 UTC')

        self.assertEqual(str(UTCOffset(minutes=12)), '+0:12:00 UTC')

        self.assertEqual(str(UTCOffset(minutes=-12)), '-0:12:00 UTC')

        self.assertEqual(str(UTCOffset(minutes=83)), '+1:23:00 UTC')

        self.assertEqual(str(UTCOffset(minutes=-83)), '-1:23:00 UTC')

        self.assertEqual(str(UTCOffset(minutes=1440)), '+1 day, 0:00:00 UTC')

        self.assertEqual(str(UTCOffset(minutes=-1440)), '-1 day, 0:00:00 UTC')

        self.assertEqual(str(UTCOffset(minutes=2967)), '+2 days, 1:27:00 UTC')

        self.assertEqual(str(UTCOffset(minutes=-2967)), '-2 days, 1:27:00 UTC')

    def test_dst(self):
        tzinfoobject = UTCOffset(minutes=240)
        #This would raise ISOFormatError or a TypeError if dst info is invalid
        result = datetime.datetime.now(tzinfoobject)
        #Hacky way to make sure the tzinfo is what we'd expect
        self.assertEqual(result.tzinfo.utcoffset(None), datetime.timedelta(hours=4))
