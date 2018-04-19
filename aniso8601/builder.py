# -*- coding: utf-8 -*-

# Copyright (c) 2016, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime

from aniso8601.exceptions import RelativeValueError

class BaseTimeBuilder(object):
    @classmethod
    def build_date(cls, year, month, day):
        raise NotImplementedError

    @classmethod
    def build_time(cls, hours=0, minutes=0, seconds=0, microseconds=0, tzinfo=None):
        raise NotImplementedError

    @classmethod
    def build_datetime(cls, year, month, day, hours=0, minutes=0, seconds=0, microseconds=0, tzinfo=None):
        raise NotImplementedError

    @classmethod
    def build_timedelta(cls, years=0, months=0, days=0, weeks=0, hours=0, minutes=0, seconds=0, milliseconds=0, microseconds=0):
        raise NotImplementedError

    @classmethod
    def combine(cls, date, time):
        raise NotImplementedError

class PythonTimeBuilder(BaseTimeBuilder):
    @classmethod
    def build_date(cls, year, month, day):
        return datetime.date(year, month, day)

    @classmethod
    def build_time(cls, hours=0, minutes=0, seconds=0, microseconds=0, tzinfo=None):
        #Builds a time from the given parts, handling fractional arguments where necessary
        fractional_hours = 0
        fractional_minutes = 0
        fractional_seconds = 0
        fractional_microseconds = 0

        if int(hours) != hours:
            fractional_hours = hours
            hours = 0
        else:
            hours = int(hours)

        if int(minutes) != minutes:
            fractional_minutes = minutes
            minutes = 0
        else:
            minutes = int(minutes)

        if int(seconds) != seconds:
            fractional_seconds = _truncate(seconds, 6)
            seconds = 0
        else:
            seconds = int(seconds)

        if int(microseconds) != microseconds:
            fractional_microseconds = microseconds
            microseconds = 0
        else:
            microseconds = int(microseconds)

        #Datetimes don't handle fractional components, so we use a timedelta
        result_datetime = datetime.datetime(1, 1, 1, hour=hours, minute=minutes, second=seconds, microsecond=microseconds, tzinfo=tzinfo) + cls.build_timedelta(seconds=fractional_seconds, microseconds=fractional_microseconds, minutes=fractional_minutes, hours=fractional_hours)

        if tzinfo is None:
            return result_datetime.time()

        return result_datetime.timetz()

    @classmethod
    def build_datetime(cls, year, month, day, hours=0, minutes=0, seconds=0, microseconds=0, tzinfo=None):
        #Builds a datetime from the given parts, handling fractional arguments where necessary
        date = datetime.date(year, month, day)
        time = cls.build_time(hours=hours, minutes=minutes, seconds=seconds, microseconds=microseconds, tzinfo=tzinfo)

        return cls.combine(date, time)

    @classmethod
    def build_timedelta(cls, years=0, months=0, days=0, weeks=0, hours=0, minutes=0, seconds=0, milliseconds=0, microseconds=0):
        #Note that weeks can be handled without conversion to days
        totaldays = years * 365 + months * 30 + days

        return datetime.timedelta(days=totaldays, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)

    @classmethod
    def combine(cls, date, time):
        return datetime.datetime.combine(date, time)

class RelativeTimeBuilder(PythonTimeBuilder):
    @classmethod
    def build_timedelta(cls, years=0, months=0, days=0, weeks=0, hours=0, minutes=0, seconds=0, milliseconds=0, microseconds=0):
        try:
            import dateutil.relativedelta

            if int(years) != years or int(months) != months:
                #https://github.com/dateutil/dateutil/issues/40
                raise RelativeValueError('Fractional months and years are not defined for relative intervals.')

            if milliseconds != 0:
                fractional_seconds = seconds + (milliseconds / 1000.0)
            else:
                fractional_seconds = seconds

            return dateutil.relativedelta.relativedelta(years=int(years), months=int(months), weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=fractional_seconds, microseconds=microseconds)
        except ImportError:
            raise RuntimeError('dateutil must be installed for relativedelta support.')

def _truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding

    https://stackoverflow.com/a/783927
    '''
    s = '%.12f' % f
    i, _, d = s.partition('.')
    return float('.'.join([i, (d + '0' * n)[:n]]))
