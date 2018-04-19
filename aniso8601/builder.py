# -*- coding: utf-8 -*-

# Copyright (c) 2016, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime

from decimal import Decimal
from aniso8601.exceptions import RelativeValueError
from aniso8601.util import decimal_split, decimal_truncate

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
        fractional_hours = Decimal(0)
        fractional_minutes = Decimal(0)
        fractional_seconds = Decimal(0)

        if int(hours) != hours:
            fractional_hours, hours = decimal_split(hours)
            hours = int(hours)
        else:
            hours = int(hours)

        if int(minutes) != minutes:
            fractional_minutes, minutes = decimal_split(minutes)
            minutes = int(minutes)
        else:
            minutes = int(minutes)

        if int(seconds) != seconds:
            fractional_seconds, seconds = decimal_split(seconds)
            seconds = int(seconds)
        else:
            seconds = int(seconds)

        #No fractional microseconds
        microseconds = int(microseconds)

        #Combine fractions
        fractional_seconds += (fractional_hours * 60 * 60) + (fractional_minutes * 60)

        #Truncate to microsecond resolution and cast to float
        fractional_seconds = float(decimal_truncate(fractional_seconds, 6))

        #Datetimes don't handle fractional components, so we use a timedelta
        result_datetime = datetime.datetime(1, 1, 1, hour=hours, minute=minutes, second=seconds, microsecond=microseconds, tzinfo=tzinfo) + cls.build_timedelta(seconds=fractional_seconds)

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
        totaldays = float(years * 365 + months * 30 + days)

        if int(weeks) != weeks:
            weeks = float(weeks)
        else:
            weeks = int(weeks)

        if int(hours) != hours:
            hours = float(hours)
        else:
            hours = int(hours)

        if int(minutes) != minutes:
            minutes = float(minutes)
        else:
            minutes = int(minutes)

        if int(seconds) != seconds:
            seconds = float(seconds)
        else:
            seconds = int(seconds)

        if int(milliseconds) != milliseconds:
            milliseconds = float(milliseconds)
        else:
            milliseconds = int(milliseconds)

        if int(microseconds) != microseconds:
            microseconds = float(microseconds)
        else:
            microseconds = int(microseconds)


        return datetime.timedelta(days=totaldays, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)

    @classmethod
    def combine(cls, date, time):
        return datetime.datetime.combine(date, time)

class RelativeTimeBuilder(PythonTimeBuilder):
    @classmethod
    def build_timedelta(cls, years=0, months=0, days=0, weeks=0, hours=0, minutes=0, seconds=0, milliseconds=0, microseconds=0):
        try:
            import dateutil.relativedelta
        except ImportError:
            raise RuntimeError('dateutil must be installed for relativedelta support.')

        if int(years) != years or int(months) != months:
            #https://github.com/dateutil/dateutil/issues/40
            raise RelativeValueError('Fractional months and years are not defined for relative intervals.')

        years = int(years)
        months = int(months)

        if int(days) != days:
            days = float(days)
        else:
            days = int(days)

        if int(weeks) != weeks:
            weeks = float(weeks)
        else:
            weeks = int(weeks)

        if int(hours) != hours:
            hours = float(hours)
        else:
            hours = int(hours)

        if int(minutes) != minutes:
            minutes = float(minutes)
        else:
            minutes = int(minutes)

        if int(seconds) != seconds:
            seconds = float(seconds)
        else:
            seconds = int(seconds)

        if milliseconds != 0:
            #Milliseconds are added to microseconds
            microseconds += milliseconds * Decimal(1e3)

        if int(microseconds) != microseconds:
            microseconds = float(microseconds)
        else:
            microseconds = int(microseconds)

        return dateutil.relativedelta.relativedelta(years=int(years), months=int(months), weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds, microseconds=microseconds)
