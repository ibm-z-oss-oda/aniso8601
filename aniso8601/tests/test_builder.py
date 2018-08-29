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
from aniso8601.builder import BaseTimeBuilder, PythonTimeBuilder, \
        RelativeTimeBuilder, TupleBuilder, UTCOffset
from aniso8601.exceptions import DayOutOfBoundsError, HoursOutOfBoundsError, \
        ISOFormatError, LeapSecondError, MidnightBoundsError, \
        MinutesOutOfBoundsError, RelativeValueError, SecondsOutOfBoundsError, \
        WeekOutOfBoundsError, YearOutOfBoundsError

class TestBaseTimeBuilder(unittest.TestCase):
    def test_build_date(self):
        with self.assertRaises(NotImplementedError):
            BaseTimeBuilder.build_date()

    def test_build_time(self):
        with self.assertRaises(NotImplementedError):
            BaseTimeBuilder.build_time()

    def test_build_datetime(self):
        with self.assertRaises(NotImplementedError):
            BaseTimeBuilder.build_datetime(None, None)

    def test_build_duration(self):
        with self.assertRaises(NotImplementedError):
            BaseTimeBuilder.build_duration()

    def test_build_interval(self):
        with self.assertRaises(NotImplementedError):
            BaseTimeBuilder.build_interval()

    def test_build_repeating_interval(self):
        with self.assertRaises(NotImplementedError):
            BaseTimeBuilder.build_repeating_interval()

    def test_build_timezone(self):
        with self.assertRaises(NotImplementedError):
            BaseTimeBuilder.build_timezone()

    def test_cast(self):
        self.assertEqual(BaseTimeBuilder.cast('1', int), 1)
        self.assertEqual(BaseTimeBuilder.cast('-2', int), -2)
        self.assertEqual(BaseTimeBuilder.cast('3', float), float(3))
        self.assertEqual(BaseTimeBuilder.cast('-4', float), float(-4))
        self.assertEqual(BaseTimeBuilder.cast('5.6', float), 5.6)
        self.assertEqual(BaseTimeBuilder.cast('-7.8', float), -7.8)

    def test_cast_exception(self):
        with self.assertRaises(ISOFormatError):
            BaseTimeBuilder.cast('asdf', int)

        with self.assertRaises(ISOFormatError):
            BaseTimeBuilder.cast('asdf', float)

    def test_cast_caughtexception(self):
        def tester(value):
            raise RuntimeError

        with self.assertRaises(ISOFormatError):
            BaseTimeBuilder.cast('asdf', tester, caughtexceptions=(RuntimeError,))

    def test_cast_thrownexception(self):
        with self.assertRaises(RuntimeError):
            BaseTimeBuilder.cast('asdf', int, thrownexception=RuntimeError)

class TestTupleBuilder(unittest.TestCase):
    def test_build_date(self):
        datetuple = TupleBuilder.build_date()
        self.assertEqual(datetuple, (None, None, None, None, None, None, 'date'))

        datetuple = TupleBuilder.build_date(YYYY='1', MM='2', DD='3', Www='4', D='5', DDD='6')
        self.assertEqual(datetuple, ('1', '2', '3', '4', '5', '6', 'date'))

    def test_build_time(self):
        timetuple = TupleBuilder.build_time()
        self.assertEqual(timetuple, (None, None, None, None, 'time'))

        timetuple = TupleBuilder.build_time(hh='1', mm='2', ss='3', tz=None)
        self.assertEqual(timetuple, ('1', '2', '3', None, 'time'))

        timetuple = TupleBuilder.build_time(hh='1', mm='2', ss='3', tz=(False, False, '4', '5', 'tz name', 'timezone'))
        self.assertEqual(timetuple, ('1', '2', '3', (False, False, '4', '5', 'tz name', 'timezone'), 'time'))

    def test_build_datetime(self):
        datetimetuple = TupleBuilder.build_datetime(('1', '2', '3', '4', '5', '6', 'date'), ('7', '8', '9', None, 'time'))
        self.assertEqual(datetimetuple, (('1', '2', '3', '4', '5', '6', 'date'), ('7', '8', '9', None, 'time'), 'datetime'))

        datetimetuple = TupleBuilder.build_datetime(('1', '2', '3', '4', '5', '6', 'date'), ('7', '8', '9', (True, False, '10', '11', 'tz name', 'timezone'), 'time'))
        self.assertEqual(datetimetuple, (('1', '2', '3', '4', '5', '6', 'date'), ('7', '8', '9', (True, False, '10', '11', 'tz name', 'timezone'), 'time'), 'datetime'))

    def test_build_duration(self):
        durationtuple = TupleBuilder.build_duration()
        self.assertEqual(durationtuple, (None, None, None, None, None, None, None, 'duration'))

        durationtuple = TupleBuilder.build_duration(PnY='1', PnM='2', PnW='3', PnD='4', TnH='5', TnM='6', TnS='7')
        self.assertEqual(durationtuple, ('1', '2', '3', '4', '5', '6', '7', 'duration'))

    def test_build_interval(self):
        intervaltuple = TupleBuilder.build_interval()
        self.assertEqual(intervaltuple, (None, None, None, 'interval'))

        intervaltuple = TupleBuilder.build_interval(start=('1', '2', '3', '4', '5', '6', 'date'), end=('7', '8', '9', '10', '11', '12', 'date'))
        self.assertEqual(intervaltuple, (('1', '2', '3', '4', '5', '6', 'date'), ('7', '8', '9', '10', '11', '12', 'date'), None, 'interval'))

        intervaltuple = TupleBuilder.build_interval(start=('1', '2', '3', (True, False, '7', '8', 'tz name', 'timezone'), 'time'), end=('4', '5', '6', (False, False, '9', '10', 'tz name', 'timezone'), 'time'))
        self.assertEqual(intervaltuple, (('1', '2', '3', (True, False, '7', '8', 'tz name', 'timezone'), 'time'), ('4', '5', '6', (False, False, '9', '10', 'tz name', 'timezone'), 'time'), None, 'interval'))

        intervaltuple = TupleBuilder.build_interval(start=(('1', '2', '3', '4', '5', '6', 'date'), ('7', '8', '9', (True, False, '10', '11', 'tz name', 'timezone'), 'time'), 'datetime'), end=(('12', '13', '14', '15', '16', '17', 'date'), ('18', '19', '20', (False, False, '21', '22', 'tz name', 'timezone'), 'time'), 'datetime'))
        self.assertEqual(intervaltuple, ((('1', '2', '3', '4', '5', '6', 'date'), ('7', '8', '9', (True, False, '10', '11', 'tz name', 'timezone'), 'time'), 'datetime'), (('12', '13', '14', '15', '16', '17', 'date'), ('18', '19', '20', (False, False, '21', '22', 'tz name', 'timezone'), 'time'), 'datetime'), None, 'interval'))

        intervaltuple = TupleBuilder.build_interval(start=('1', '2', '3', '4', '5', '6', 'date'), end=None, duration=('7', '8', '9', '10', '11', '12', '13', 'duration'))
        self.assertEqual(intervaltuple, (('1', '2', '3', '4', '5', '6', 'date'), None, ('7', '8', '9', '10', '11', '12', '13', 'duration'), 'interval'))

        intervaltuple = TupleBuilder.build_interval(start=None, end=('1', '2', '3', (True, False, '4', '5', 'tz name', 'timezone'), 'time'), duration=('6', '7', '8', '9', '10', '11', '12', 'duration'))
        self.assertEqual(intervaltuple, (None, ('1', '2', '3', (True, False, '4', '5', 'tz name', 'timezone'), 'time'), ('6', '7', '8', '9', '10', '11', '12', 'duration'), 'interval'))

    def test_build_repeating_interval(self):
        intervaltuple = TupleBuilder.build_repeating_interval()
        self.assertEqual(intervaltuple, (None, None, None, 'repeatinginterval'))

        intervaltuple = TupleBuilder.build_repeating_interval(R=True, interval=(('1', '2', '3', '4', '5', '6', 'date'), ('7', '8', '9', '10', '11', '12', 'date'), None, 'interval'))
        self.assertEqual(intervaltuple, (True, None, (('1', '2', '3', '4', '5', '6', 'date'), ('7', '8', '9', '10', '11', '12', 'date'), None, 'interval'), 'repeatinginterval'))

        intervaltuple = TupleBuilder.build_repeating_interval(R=False, Rnn='1', interval=((('2', '3', '4', '5', '6', '7', 'date'), ('8', '9', '10', None, 'time'), 'datetime'), (('11', '12', '13', '14', '15', '16', 'date'), ('17', '18', '19', None, 'time'), 'datetime'), None, 'interval'))
        self.assertEqual(intervaltuple, (False, '1', ((('2', '3', '4', '5', '6', '7', 'date'), ('8', '9', '10', None, 'time'), 'datetime'), (('11', '12', '13', '14', '15', '16', 'date'), ('17', '18', '19', None, 'time'), 'datetime'), None, 'interval'), 'repeatinginterval'))

    def test_build_timezone(self):
        tztuple = TupleBuilder.build_timezone()
        self.assertEqual(tztuple, (None, None, None, None, '', 'timezone'))

        tztuple = TupleBuilder.build_timezone(negative=False, Z=True, name='UTC')
        self.assertEqual(tztuple, (False, True, None, None, 'UTC', 'timezone'))

        tztuple = TupleBuilder.build_timezone(negative=False, Z=False, hh='1', mm='2', name='+01:02')
        self.assertEqual(tztuple, (False, False, '1', '2', '+01:02', 'timezone'))

        tztuple = TupleBuilder.build_timezone(negative=True, Z=False, hh='1', mm='2', name='-01:02')
        self.assertEqual(tztuple, (True, False, '1', '2', '-01:02', 'timezone'))

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

        #Make sure we shift in zeros
        date = PythonTimeBuilder.build_date(YYYY='1', MM=None, DD=None, Www=None, D=None, DDD=None)
        self.assertEqual(date, datetime.date(1000, 1, 1))

        date = PythonTimeBuilder.build_date(YYYY='12', MM=None, DD=None, Www=None, D=None, DDD=None)
        self.assertEqual(date, datetime.date(1200, 1, 1))

        date = PythonTimeBuilder.build_date(YYYY='123', MM=None, DD=None, Www=None, D=None, DDD=None)
        self.assertEqual(date, datetime.date(1230, 1, 1))

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
        self.assertEqual(PythonTimeBuilder.build_datetime(('1234', '2', '3', None, None, None, 'date'), ('23', '21', '28.512400', None, 'time')), datetime.datetime(1234, 2, 3, hour=23, minute=21, second=28, microsecond=512400))

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
        duration = PythonTimeBuilder.build_duration(PnY='1', PnM='2', PnD='3', TnH='4', TnM='54', TnS='6')
        self.assertEqual(duration, datetime.timedelta(days=428, seconds=17646))

        duration = PythonTimeBuilder.build_duration(PnY='1', PnM='2', PnD='3', TnH='4', TnM='54', TnS='6.5')
        self.assertEqual(duration, datetime.timedelta(days=428, seconds=17646.5))

        duration = PythonTimeBuilder.build_duration(PnY='1', PnM='2', PnD='3', TnH='4', TnM='54', TnS='6')
        self.assertEqual(duration, datetime.timedelta(days=428, hours=4, minutes=54, seconds=6))

        duration = PythonTimeBuilder.build_duration(PnY='1', PnM='2', PnD='3', TnH='4', TnM='54', TnS='6.5')
        self.assertEqual(duration, datetime.timedelta(days=428, hours=4, minutes=54, seconds=6.5))

        duration = PythonTimeBuilder.build_duration(PnY='1', PnM='2', PnD='3')
        self.assertEqual(duration, datetime.timedelta(days=428))

        duration = PythonTimeBuilder.build_duration(PnY='1', PnM='2', PnD='3.5')
        self.assertEqual(duration, datetime.timedelta(days=428.5))

        duration = PythonTimeBuilder.build_duration(TnH='4', TnM='54', TnS='6.5')
        self.assertEqual(duration, datetime.timedelta(hours=4, minutes=54, seconds=6.5))

        #Make sure we truncate, not round
        #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
        duration = PythonTimeBuilder.build_duration(TnS='0.0000001')
        self.assertEqual(duration, datetime.timedelta(0))

        duration = PythonTimeBuilder.build_duration(TnS='2.0000048')
        self.assertEqual(duration, datetime.timedelta(seconds=2, microseconds=4))

        duration = PythonTimeBuilder.build_duration(PnY='1')
        self.assertEqual(duration, datetime.timedelta(days=365))

        duration = PythonTimeBuilder.build_duration(PnY='1.5')
        self.assertEqual(duration, datetime.timedelta(days=547.5))

        duration = PythonTimeBuilder.build_duration(PnM='1')
        self.assertEqual(duration, datetime.timedelta(days=30))

        duration = PythonTimeBuilder.build_duration(PnM='1.5')
        self.assertEqual(duration, datetime.timedelta(days=45))

        duration = PythonTimeBuilder.build_duration(PnW='1')
        self.assertEqual(duration, datetime.timedelta(days=7))

        duration = PythonTimeBuilder.build_duration(PnW='1.5')
        self.assertEqual(duration, datetime.timedelta(days=10.5))

        duration = PythonTimeBuilder.build_duration(PnD='1')
        self.assertEqual(duration, datetime.timedelta(days=1))

        duration = PythonTimeBuilder.build_duration(PnD='1.5')
        self.assertEqual(duration, datetime.timedelta(days=1.5))

        duration = PythonTimeBuilder.build_duration(PnY='0003', PnM='06', PnD='04', TnH='12', TnM='30', TnS='05')
        self.assertEqual(duration, datetime.timedelta(days=1279, hours=12, minutes=30, seconds=5))

        duration = PythonTimeBuilder.build_duration(PnY='0003', PnM='06', PnD='04', TnH='12', TnM='30', TnS='05.5')
        self.assertEqual(duration, datetime.timedelta(days=1279, hours=12, minutes=30, seconds=5.5))

        duration = PythonTimeBuilder.build_duration(PnY='0003', PnM='06', PnD='04', TnH='12', TnM='30', TnS='05')
        self.assertEqual(duration, datetime.timedelta(days=1279, hours=12, minutes=30, seconds=5))

        duration = PythonTimeBuilder.build_duration(PnY='0003', PnM='06', PnD='04', TnH='12', TnM='30', TnS='05.5')
        self.assertEqual(duration, datetime.timedelta(days=1279, hours=12, minutes=30, seconds=5.5))

        #Make sure we truncate, not round
        #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
        duration = PythonTimeBuilder.build_duration(PnY='0001', PnM='02', PnD='03', TnH='14', TnM='43', TnS='59.9999997')
        self.assertEqual(duration, datetime.timedelta(days=428, hours=14, minutes=43, seconds=59, microseconds=999999))

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

    def test_build_object(self):
        resultdate = PythonTimeBuilder._build_object(('1234', '5', '6', None, None, None, 'date'))
        self.assertEqual(resultdate, datetime.date(year=1234, month=5, day=6))

        resultdate = PythonTimeBuilder._build_object(('1234', None, None, '6', '7', None, 'date'))
        self.assertEqual(resultdate, datetime.date(year=1234, month=2, day=12))

        resultdate = PythonTimeBuilder._build_object(('1234', None, None, None, None, '6', 'date'))
        self.assertEqual(resultdate, datetime.date(year=1234, month=1, day=6))

        resulttime = PythonTimeBuilder._build_object(('1', '2', '3', (False, False, '4', '5', 'tz name', 'timezone'), 'time'))
        self.assertEqual(resulttime, datetime.time(hour=1, minute=2, second=3, tzinfo=UTCOffset(name='tzname', minutes=245)))

        resultdatetime = PythonTimeBuilder._build_object((('1234', '5', '6', None, None, None, 'date'), ('7', '8', '9', None, 'time'), 'datetime'))
        self.assertEqual(resultdatetime, datetime.datetime(year=1234, month=5, day=6, hour=7, minute=8, second=9))

        resultduration = PythonTimeBuilder._build_object(('1', '2', '3', '4', '5', '6', '7', 'duration'))
        self.assertEqual(resultduration, datetime.timedelta(days=450, seconds=18367))

        resultinterval = PythonTimeBuilder._build_object((('1', '2', '3', None, None, None, 'date'), ('4', '5', '6', None, None, None, 'date'), None, 'interval'))
        self.assertEqual(resultinterval, (datetime.date(1000, 2, 3), datetime.date(4000, 5, 6)))

        resultinterval = PythonTimeBuilder._build_object((('1', '2', '3', None, None, None, 'date'), None, ('4', '5', None, '6', None, None, None, 'duration'), 'interval'))
        self.assertEqual(resultinterval, (datetime.date(1000, 2, 3), datetime.date(1004, 7, 8)))

        resultinterval = PythonTimeBuilder._build_object( (None, (('1', '2', '3', None, None, None, 'date'), ('4', '5', '6', None, 'time'), 'datetime'), (None, None, None, None, '7', '8', '9', 'duration'), 'interval'))
        self.assertEqual(resultinterval, (datetime.datetime(year=1000, month=2, day=3, hour=4, minute=5, second=6), datetime.datetime(year=1000, month=2, day=2, hour=20, minute=56, second=57)))

        results = list(PythonTimeBuilder._build_object((False, '10', (('1', '2', '3', None, None, None, 'date'), None, (None, None, None, '4', None, None, None, 'duration'), 'interval'), 'repeatinginterval')))

        for dateindex in compat.range(0, 10):
             self.assertEqual(results[dateindex], datetime.date(year=1000, month=2, day=3) + dateindex * datetime.timedelta(days=4))

        resultgenerator = PythonTimeBuilder._build_object((True, None, (None, ('1', '2', '3', None, None, None, 'date'), (None, None, None, '4', None, None, None, 'duration'), 'interval'), 'repeatinginterval'))

        #Check the first 10
        for dateindex in compat.range(0, 10):
             self.assertEqual(next(resultgenerator), datetime.date(year=1000, month=2, day=3) - dateindex * datetime.timedelta(days=4))

        resulttimezone = PythonTimeBuilder._build_object((False, True, None, None, 'UTC', 'timezone'))
        self.assertEqual(resulttimezone.utcoffset(None), datetime.timedelta(hours=0))
        self.assertEqual(resulttimezone.tzname(None), 'UTC')

        resulttimezone = PythonTimeBuilder._build_object((False, False, '1', '2', '+01:02', 'timezone'))
        self.assertEqual(resulttimezone.utcoffset(None), datetime.timedelta(hours=1, minutes=2))
        self.assertEqual(resulttimezone.tzname(None), '+01:02')

        resulttimezone = PythonTimeBuilder._build_object((True, False, '1', '2', '-01:02', 'timezone'))
        self.assertEqual(resulttimezone.utcoffset(None), -datetime.timedelta(hours=1, minutes=2))
        self.assertEqual(resulttimezone.tzname(None), '-01:02')

    def test_build_week_date(self):
        weekdate = PythonTimeBuilder._build_week_date(2009, 1)
        self.assertEqual(weekdate, datetime.date(year=2008, month=12, day=29))

        weekdate = PythonTimeBuilder._build_week_date(2009, 53, isoday=7)
        self.assertEqual(weekdate, datetime.date(year=2010, month=1, day=3))

    def test_build_ordinal_date(self):
        ordinaldate = PythonTimeBuilder._build_ordinal_date(1981, 95)
        self.assertEqual(ordinaldate, datetime.date(year=1981, month=4, day=5))

    def test_build_ordinal_date_bounds_checking(self):
        with self.assertRaises(DayOutOfBoundsError):
            PythonTimeBuilder._build_ordinal_date(1234, 0)

        with self.assertRaises(DayOutOfBoundsError):
            PythonTimeBuilder._build_ordinal_date(1234, 367)

    def test_iso_year_start(self):
        yearstart = PythonTimeBuilder._iso_year_start(2004)
        self.assertEqual(yearstart, datetime.date(year=2003, month=12, day=29))

        yearstart = PythonTimeBuilder._iso_year_start(2010)
        self.assertEqual(yearstart, datetime.date(year=2010, month=1, day=4))

        yearstart = PythonTimeBuilder._iso_year_start(2009)
        self.assertEqual(yearstart, datetime.date(year=2008, month=12, day=29))

    def test_date_generator(self):
        results = list(PythonTimeBuilder._date_generator(datetime.date(year=2018, month=8, day=29), datetime.timedelta(days=1), 10))

        for dateindex in compat.range(0, 10):
             self.assertEqual(results[dateindex], datetime.date(year=2018, month=8, day=29) + dateindex * datetime.timedelta(days=1))

    def test_date_generator_unbounded(self):
        resultgenerator = PythonTimeBuilder._date_generator_unbounded(datetime.date(year=2018, month=8, day=29), datetime.timedelta(days=5))

        #Check the first time
        for dateindex in compat.range(0, 10):
             self.assertEqual(next(resultgenerator), datetime.date(year=2018, month=8, day=29) + dateindex * datetime.timedelta(days=5))

class TestRelativeTimeBuilder(unittest.TestCase):
    def test_build_duration(self):
        duration = RelativeTimeBuilder.build_duration(PnY='1')
        self.assertEqual(duration, dateutil.relativedelta.relativedelta(years=1))

        duration = RelativeTimeBuilder.build_duration(PnM='1')
        self.assertEqual(duration, dateutil.relativedelta.relativedelta(months=1))

        #Add the relative ‘days’ argument to the absolute day. Notice that the ‘weeks’ argument is multiplied by 7 and added to ‘days’.
        #http://dateutil.readthedocs.org/en/latest/relativedelta.html
        duration = RelativeTimeBuilder.build_duration(PnW='1')
        self.assertEqual(duration, dateutil.relativedelta.relativedelta(days=7))

        duration = RelativeTimeBuilder.build_duration(PnW='1.5')
        self.assertEqual(duration, dateutil.relativedelta.relativedelta(days=10.5))

        duration = RelativeTimeBuilder.build_duration(PnD='1')
        self.assertEqual(duration, dateutil.relativedelta.relativedelta(days=1))

        duration = RelativeTimeBuilder.build_duration(PnD='1.5')
        self.assertEqual(duration, dateutil.relativedelta.relativedelta(days=1.5))

        duration = RelativeTimeBuilder.build_duration(PnY='1', PnM='2', PnD='3')
        self.assertEqual(duration, dateutil.relativedelta.relativedelta(years=1, months=2, days=3))

        duration = RelativeTimeBuilder.build_duration(PnY='1', PnM='2', PnD='3.5')
        self.assertEqual(duration, dateutil.relativedelta.relativedelta(years=1, months=2, days=3.5))

        duration = RelativeTimeBuilder.build_duration(PnY='1', PnM='2', PnD='3', TnH='4', TnM='54', TnS='6.5')
        self.assertEqual(duration, dateutil.relativedelta.relativedelta(years=1, months=2, days=3, hours=4, minutes=54, seconds=6, microseconds=500000))

        duration = RelativeTimeBuilder.build_duration(PnY='0003', PnM='06', PnD='04', TnH='12', TnM='30', TnS='05')
        self.assertEqual(duration, dateutil.relativedelta.relativedelta(years=3, months=6, days=4, hours=12, minutes=30, seconds=5))

        duration = RelativeTimeBuilder.build_duration(PnY='0003', PnM='06', PnD='04', TnH='12', TnM='30', TnS='05.5')
        self.assertEqual(duration, dateutil.relativedelta.relativedelta(years=3, months=6, days=4, hours=12, minutes=30, seconds=5, microseconds=500000))

        duration = RelativeTimeBuilder.build_duration(TnH='4', TnM='54', TnS='6.5')
        self.assertEqual(duration, dateutil.relativedelta.relativedelta(hours=4, minutes=54, seconds=6, microseconds=500000))

        #Make sure we truncate, not round
        #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
        duration = RelativeTimeBuilder.build_duration(TnS='0.0000001')
        self.assertEqual(duration, dateutil.relativedelta.relativedelta(0))

        duration = RelativeTimeBuilder.build_duration(TnS='2.0000048')
        self.assertEqual(duration, dateutil.relativedelta.relativedelta(seconds=2, microseconds=4))

        duration = RelativeTimeBuilder.build_duration(PnY='0001', PnM='02', PnD='03', TnH='14', TnM='43', TnS='59.9999997')
        self.assertEqual(duration, dateutil.relativedelta.relativedelta(years=1, months=2, days=3, hours=14, minutes=43, seconds=59, microseconds=999999))

        duration = RelativeTimeBuilder.build_duration(PnY='1', PnM='2', PnW='4', PnD='3', TnH='5', TnM='6', TnS='7.0000091011')
        self.assertEqual(duration, dateutil.relativedelta.relativedelta(years=1, months=2, days=31, hours=5, minutes=6, seconds=7, microseconds=9))

    def test_build_duration_fractional_year(self):
        with self.assertRaises(RelativeValueError):
            RelativeTimeBuilder.build_duration(PnY='1.5')

    def test_build_duration_fractional_month(self):
        with self.assertRaises(RelativeValueError):
            RelativeTimeBuilder.build_duration(PnM='1.5')

    def test_build_duration_nodateutil(self):
        import sys
        import dateutil

        dateutil_import = dateutil

        sys.modules['dateutil'] = None

        with self.assertRaises(RuntimeError):
            RelativeTimeBuilder.build_duration(PnY='1', PnM='2', PnW='3', PnD='4', TnH='5', TnM='6', TnS='7')

        #Reinstall dateutil
        sys.modules['dateutil'] = dateutil_import

    def test_build_interval(self):
        #Intervals are contingent on durations, make sure they work
        interval = RelativeTimeBuilder.build_interval(end=(('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), duration=(None, '1', None, None, None, None, None, 'duration'))
        self.assertEqual(interval[0], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))
        self.assertEqual(interval[1], datetime.datetime(year=1981, month=3, day=5, hour=1, minute=1))

        interval = RelativeTimeBuilder.build_interval(end=('1981', '04', '05', None, None, None, 'date'), duration=(None, '1', None, None, None, None, None, 'duration'))
        self.assertEqual(interval[0], datetime.date(year=1981, month=4, day=5))
        self.assertEqual(interval[1], datetime.date(year=1981, month=3, day=5))

        interval = RelativeTimeBuilder.build_interval(end=('2014', '11', '12', None, None, None, 'date'), duration=(None, None, None, None, '1', None, None, 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2014, month=11, day=12))
        self.assertEqual(interval[1], datetime.datetime(year=2014, month=11, day=11, hour=23))

        interval = RelativeTimeBuilder.build_interval(end=('2014', '11', '12', None, None, None, 'date'), duration=(None, None, None, None, '4', '54', '6.5', 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2014, month=11, day=12))
        self.assertEqual(interval[1], datetime.datetime(year=2014, month=11, day=11, hour=19, minute=5, second=53, microsecond=500000))

        #Make sure we truncate, not round
        #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
        interval = RelativeTimeBuilder.build_interval(end=('2018', '03', '06', None, None, None, 'date'), duration=(None, None, None, None, None, None, '0.0000001', 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2018, month=3, day=6))
        self.assertEqual(interval[1], datetime.datetime(year=2018, month=3, day=6))

        interval = RelativeTimeBuilder.build_interval(end=('2018', '03', '06', None, None, None, 'date'), duration=(None, None, None, None, None, None, '2.0000048', 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2018, month=3, day=6))
        self.assertEqual(interval[1], datetime.datetime(year=2018, month=3, day=5, hour=23, minute=59, second=57, microsecond=999996))

        interval = RelativeTimeBuilder.build_interval(start=('2018', '03', '06', None, None, None, 'date'), duration=(None, None, None, None, None, None, '0.0000001', 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2018, month=3, day=6))
        self.assertEqual(interval[1], datetime.datetime(year=2018, month=3, day=6))

        interval = RelativeTimeBuilder.build_interval(start=('2018', '03', '06', None, None, None, 'date'), duration=(None, None, None, None, None, None, '2.0000048', 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2018, month=3, day=6))
        self.assertEqual(interval[1], datetime.datetime(year=2018, month=3, day=6, hour=0, minute=0, second=2, microsecond=4))

        interval = RelativeTimeBuilder.build_interval(start=(('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), duration=(None, '1', None, '1', None, '1', None, 'duration'))
        self.assertEqual(interval[0], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))
        self.assertEqual(interval[1], datetime.datetime(year=1981, month=5, day=6, hour=1, minute=2))

        interval = RelativeTimeBuilder.build_interval(start=('1981', '04', '05', None, None, None, 'date'), duration=(None, '1', None, '1', None, None, None, 'duration'))
        self.assertEqual(interval[0], datetime.date(year=1981, month=4, day=5))
        self.assertEqual(interval[1], datetime.date(year=1981, month=5, day=6))

        interval = RelativeTimeBuilder.build_interval(start=('2014', '11', '12', None, None, None, 'date'), duration=(None, None, None, None, '1', None, None, 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2014, month=11, day=12))
        self.assertEqual(interval[1], datetime.datetime(year=2014, month=11, day=12, hour=1, minute=0))

        interval = RelativeTimeBuilder.build_interval(start=('2014', '11', '12', None, None, None, 'date'), duration=(None, None, None, None, '4', '54', '6.5', 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2014, month=11, day=12))
        self.assertEqual(interval[1], datetime.datetime(year=2014, month=11, day=12, hour=4, minute=54, second=6, microsecond=500000))

        interval = RelativeTimeBuilder.build_interval(start=(('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00.0000001', None, 'time'), 'datetime'), end=(('1981', '04', '05', None, None, None, 'date'), ('14', '43', '59.9999997', None, 'time'), 'datetime'))
        self.assertEqual(interval[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(interval[1], datetime.datetime(year=1981, month=4, day=5, hour=14, minute=43, second=59, microsecond=999999))

        #Some relativedelta examples
        #http://dateutil.readthedocs.org/en/latest/examples.html#relativedelta-examples
        interval = RelativeTimeBuilder.build_interval(start=('2003', '1', '27', None, None, None, 'date'), duration=(None, '1', None, None, None, None, None, 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2003, month=1, day=27))
        self.assertEqual(interval[1], datetime.date(year=2003, month=2, day=27))

        interval = RelativeTimeBuilder.build_interval(start=('2003', '1', '31', None, None, None, 'date'), duration=(None, '1', None, None, None, None, None, 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2003, month=1, day=31))
        self.assertEqual(interval[1], datetime.date(year=2003, month=2, day=28))

        interval = RelativeTimeBuilder.build_interval(start=('2003', '1', '31', None, None, None, 'date'), duration=(None, '2', None, None, None, None, None, 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2003, month=1, day=31))
        self.assertEqual(interval[1], datetime.date(year=2003, month=3, day=31))

        interval = RelativeTimeBuilder.build_interval(start=('2000', '2', '28', None, None, None, 'date'), duration=('1', None, None, None, None, None, None, 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2000, month=2, day=28))
        self.assertEqual(interval[1], datetime.date(year=2001, month=2, day=28))

        interval = RelativeTimeBuilder.build_interval(start=('1999', '2', '28', None, None, None, 'date'), duration=('1', None, None, None, None, None, None, 'duration'))
        self.assertEqual(interval[0], datetime.date(year=1999, month=2, day=28))
        self.assertEqual(interval[1], datetime.date(year=2000, month=2, day=28))

        interval = RelativeTimeBuilder.build_interval(start=('1999', '3', '1', None, None, None, 'date'), duration=('1', None, None, None, None, None, None, 'duration'))
        self.assertEqual(interval[0], datetime.date(year=1999, month=3, day=1))
        self.assertEqual(interval[1], datetime.date(year=2000, month=3, day=1))

        interval = RelativeTimeBuilder.build_interval(end=('2001', '2', '28', None, None, None, 'date'), duration=('1', None, None, None, None, None, None, 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2001, month=2, day=28))
        self.assertEqual(interval[1], datetime.date(year=2000, month=2, day=28))

        interval = RelativeTimeBuilder.build_interval(end=('2001', '3', '1', None, None, None, 'date'), duration=('1', None, None, None, None, None, None, 'duration'))
        self.assertEqual(interval[0], datetime.date(year=2001, month=3, day=1))
        self.assertEqual(interval[1], datetime.date(year=2000, month=3, day=1))

        interval = RelativeTimeBuilder.build_interval(start=(('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), end=(('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'))
        self.assertEqual(interval[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(interval[1], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))

        interval = RelativeTimeBuilder.build_interval(start=(('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), end=('1981', '04', '05', None, None, None, 'date'))
        self.assertEqual(interval[0], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1))
        self.assertEqual(interval[1], datetime.date(year=1981, month=4, day=5))

        interval = RelativeTimeBuilder.build_interval(start=('1980', '03', '05', None, None, None, 'date'), end=(('1981', '04', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'))
        self.assertEqual(interval[0], datetime.date(year=1980, month=3, day=5))
        self.assertEqual(interval[1], datetime.datetime(year=1981, month=4, day=5, hour=1, minute=1))

        interval = RelativeTimeBuilder.build_interval(start=('1980', '03', '05', None, None, None, 'date'), end=('1981', '04', '05', None, None, None, 'date'))
        self.assertEqual(interval[0], datetime.date(year=1980, month=3, day=5))
        self.assertEqual(interval[1], datetime.date(year=1981, month=4, day=5))

        interval = RelativeTimeBuilder.build_interval(start=('1981', '04', '05', None, None, None, 'date'), end=('1980', '03', '05', None, None, None, 'date'))
        self.assertEqual(interval[0], datetime.date(year=1981, month=4, day=5))
        self.assertEqual(interval[1], datetime.date(year=1980, month=3, day=5))

    def test_build_repeating_interval(self):
        #Repeating intervals are contingent on durations, make sure they work
        results = list(RelativeTimeBuilder.build_repeating_interval(Rnn=3, interval=(('1981', '04', '05', None, None, None, 'date'), None, (None, None, None, '1', None, None, None, 'duration'), 'interval')))
        self.assertEqual(results[0], datetime.date(year=1981, month=4, day=5))
        self.assertEqual(results[1], datetime.date(year=1981, month=4, day=6))
        self.assertEqual(results[2], datetime.date(year=1981, month=4, day=7))

        results = list(RelativeTimeBuilder.build_repeating_interval(Rnn=11, interval=(None, (('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (None, None, None, None, '1', '2', None, 'duration'), 'interval')))

        for dateindex in compat.range(0, 11):
             self.assertEqual(results[dateindex], datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1) - dateindex * datetime.timedelta(hours=1, minutes=2))

        #Make sure relative is correctly applied for months
        #https://bitbucket.org/nielsenb/aniso8601/issues/12/month-intervals-calculated-incorrectly-or
        results = list(RelativeTimeBuilder.build_repeating_interval(Rnn=4, interval=((('2017', '04', '30', None, None, None, 'date'), ('00', '00', '00', None, 'time'), 'datetime'), None, (None, '1', None, None, None, None, None, 'duration'), 'interval')))

        self.assertEqual(results[0], datetime.datetime(year=2017, month=4, day=30))
        self.assertEqual(results[1], datetime.datetime(year=2017, month=5, day=30))
        self.assertEqual(results[2], datetime.datetime(year=2017, month=6, day=30))
        self.assertEqual(results[3], datetime.datetime(year=2017, month=7, day=30))

        resultgenerator = RelativeTimeBuilder.build_repeating_interval(R=True, interval=(None, (('1980', '03', '05', None, None, None, 'date'), ('01', '01', '00', None, 'time'), 'datetime'), (None, None, None, None, '1', '2', None, 'duration'), 'interval'))

        for dateindex in compat.range(0, 11):
             self.assertEqual(next(resultgenerator), datetime.datetime(year=1980, month=3, day=5, hour=1, minute=1) - dateindex * datetime.timedelta(hours=1, minutes=2))

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
