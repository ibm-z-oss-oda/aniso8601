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

from aniso8601.builder import BaseTimeBuilder, PythonTimeBuilder, RelativeTimeBuilder, UTCOffset
from aniso8601.exceptions import DayOutOfBoundsError, WeekOutOfBoundsError, \
        YearOutOfBoundsError

class TestBaseTimeBuilder(unittest.TestCase):
    def test_build_date(self):
        with self.assertRaises(NotImplementedError):
            BaseTimeBuilder.build_date()

    def test_build_time(self):
        with self.assertRaises(NotImplementedError):
            BaseTimeBuilder.build_time()

    def test_build_timedelta(self):
        with self.assertRaises(NotImplementedError):
            BaseTimeBuilder.build_timedelta()

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

        time = PythonTimeBuilder.build_time(hh='1', mm='23.4567')
        self.assertEqual(time, datetime.time(hour=1, minute=23, second=27, microsecond=402000))

        time = PythonTimeBuilder.build_time(hh='23', mm='21', ss='28.512400')
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400))

        time = PythonTimeBuilder.build_time(tz=UTCOffset(name='UTC', minutes=0))
        self.assertEqual(time, datetime.time(tzinfo=UTCOffset(name='UTC', minutes=0)))

        time = PythonTimeBuilder.build_time(hh='1', mm='23', tz=UTCOffset(name='+1', minutes=60))
        self.assertEqual(time, datetime.time(hour=1, minute=23, tzinfo=UTCOffset(name='+1', minutes=60)))

        time = PythonTimeBuilder.build_time(hh='1', mm='23.4567', tz=UTCOffset(name='-1', minutes=-60))
        self.assertEqual(time, datetime.time(hour=1, minute=23, second=27, microsecond=402000, tzinfo=UTCOffset(name='-1', minutes=-60)))

        time = PythonTimeBuilder.build_time(hh='23', mm='21', ss='28.512400', tz=UTCOffset(name='+1.5', minutes=90))
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='+1.5', minutes=90)))

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

    def test_build_timedelta(self):
        timedelta = PythonTimeBuilder.build_timedelta(years=1, months=2, days=3, weeks=4, hours=5, minutes=6, seconds=7, microseconds=9.1011)
        self.assertEqual(timedelta, datetime.timedelta(days=428, seconds=7, microseconds=9.1011, minutes=6, hours=5, weeks=4))

        timedelta = PythonTimeBuilder.build_timedelta(years=1, months=-2, days=3, weeks=-4, hours=5, minutes=-6, seconds=7, microseconds=9.1011)
        self.assertEqual(timedelta, datetime.timedelta(days=308, seconds=7, microseconds=9.1011, minutes=-6, hours=5, weeks=-4))

    def test_build_combine(self):
        date = datetime.date(1, 2, 3)
        time = datetime.time(hour=23, minute=21, second=28, microsecond=512400)

        self.assertEqual(PythonTimeBuilder.combine(date, time), datetime.datetime(1, 2, 3, hour=23, minute=21, second=28, microsecond=512400))

class TestRelativeTimeBuilder(unittest.TestCase):
    def test_build_date(self):
        self.assertEqual(RelativeTimeBuilder.build_date(1, 2, 3), datetime.date(1, 2, 3))

    def test_build_time(self):
        time = RelativeTimeBuilder.build_time()
        self.assertEqual(time, datetime.time())

        time = RelativeTimeBuilder.build_time(hh='1', mm='23')
        self.assertEqual(time, datetime.time(hour=1, minute=23))

        time = RelativeTimeBuilder.build_time(hh='1', mm='23.4567')
        self.assertEqual(time, datetime.time(hour=1, minute=23, second=27, microsecond=402000))

        time = RelativeTimeBuilder.build_time(hh='23', mm='21', ss='28.512400')
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400))

        time = RelativeTimeBuilder.build_time(tz=UTCOffset(name='UTC', minutes=0))
        self.assertEqual(time, datetime.time(tzinfo=UTCOffset(name='UTC', minutes=0)))

        time = RelativeTimeBuilder.build_time(hh='1', mm='23', tz=UTCOffset(name='+1', minutes=60))
        self.assertEqual(time, datetime.time(hour=1, minute=23, tzinfo=UTCOffset(name='+1', minutes=60)))

        time = RelativeTimeBuilder.build_time(hh='1', mm='23.4567', tz=UTCOffset(name='-1', minutes=-60))
        self.assertEqual(time, datetime.time(hour=1, minute=23, second=27, microsecond=402000, tzinfo=UTCOffset(name='-1', minutes=-60)))

        time = RelativeTimeBuilder.build_time(hh='23', mm='21', ss='28.512400', tz=UTCOffset(name='+1.5', minutes=90))
        self.assertEqual(time, datetime.time(hour=23, minute=21, second=28, microsecond=512400, tzinfo=UTCOffset(name='+1.5', minutes=90)))

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
