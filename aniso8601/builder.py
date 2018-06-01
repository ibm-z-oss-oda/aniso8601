# -*- coding: utf-8 -*-

# Copyright (c) 2016, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime

from aniso8601.exceptions import HoursOutOfBoundsError, ISOFormatError, \
        LeapSecondError, MidnightBoundsError, MinutesOutOfBoundsError, \
        RelativeValueError, SecondsOutOfBoundsError

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
    def build_timedelta(cls, years=0, months=0, days=0, weeks=0, hours=0, minutes=0, seconds=0, microseconds=0):
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
        float_hours = float(0)
        float_minutes = float(0)
        float_seconds = float(0)

        try:
            if '.' in str(hours):
                float_hours = float(hours)
                hours = 0

            hours = int(hours)
        except ValueError:
            raise ISOFormatError('Invalid hour string.')

        try:
            if '.' in str(minutes):
                float_minutes = float(minutes)
                minutes = 0

            minutes = int(minutes)
        except ValueError:
            raise ISOFormatError('Invalid minute string.')

        try:
            if '.' in str(seconds):
                float_seconds = float(seconds[0:str(seconds).index('.') + 7])
                seconds = 0

            seconds = int(seconds)
        except ValueError:
            raise ISOFormatError('Invalid second string.')

        #No fractional microseconds
        try:
            microseconds = int(microseconds)
        except ValueError:
            raise ISOFormatError('Invalid microsecond string.')

        #Range checks
        if hours == 23 and float_hours == 0 and minutes == 59 and float_minutes == 0 and seconds == 60 and float_seconds == 0:
            #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
            raise LeapSecondError('Leap seconds are not supported.')

        if hours == 24 and float_hours == 0 and (minutes != 0 or float_minutes != 0 or seconds != 0 or float_seconds != 0 or microseconds != 0):
            raise MidnightBoundsError('Hour 24 may only represent midnight.')

        if hours > 24 or float_hours > 24:
            raise HoursOutOfBoundsError('Hour must be between 0..24 with 24 representing midnight.')

        if minutes >= 60 or float_minutes >= 60:
            raise MinutesOutOfBoundsError('Minutes must be less than 60.')

        if seconds >= 60 or float_seconds >= 60:
            raise SecondsOutOfBoundsError('Seconds must be less than 60.')

        #Fix ranges that have passed range checks
        if hours == 24:
            hours = 0
            minutes = 0
            seconds = 0

        #Datetimes don't handle fractional components, so we use a timedelta
        result_datetime = datetime.datetime(1, 1, 1, hour=hours, minute=minutes, second=seconds, microsecond=microseconds, tzinfo=tzinfo) + cls.build_timedelta(hours=float_hours, minutes=float_minutes, seconds=float_seconds)

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
    def build_timedelta(cls, years=0, months=0, days=0, weeks=0, hours=0, minutes=0, seconds=0, microseconds=0):
        #Note that weeks can be handled without conversion to days
        totaldays = float(years * 365 + months * 30 + days)

        if '.' in str(weeks):
            weeks = float(weeks)
        else:
            weeks = int(weeks)

        if '.' in str(hours):
            hours = float(hours)
        else:
            hours = int(hours)

        if '.' in str(minutes):
            minutes = float(minutes)
        else:
            minutes = int(minutes)

        if '.' in str(seconds):
            seconds = float(seconds)
        else:
            seconds = int(seconds)

        if '.' in str(microseconds):
            microseconds = float(microseconds)
        else:
            microseconds = int(microseconds)

        return datetime.timedelta(days=totaldays, seconds=seconds, microseconds=microseconds, minutes=minutes, hours=hours, weeks=weeks)

    @classmethod
    def combine(cls, date, time):
        return datetime.datetime.combine(date, time)

class RelativeTimeBuilder(PythonTimeBuilder):
    @classmethod
    def build_timedelta(cls, years=0, months=0, days=0, weeks=0, hours=0, minutes=0, seconds=0, microseconds=0):
        try:
            import dateutil.relativedelta
        except ImportError:
            raise RuntimeError('dateutil must be installed for relativedelta support.')

        if int(years) != years or int(months) != months:
            #https://github.com/dateutil/dateutil/issues/40
            raise RelativeValueError('Fractional months and years are not defined for relative intervals.')

        years = int(years)
        months = int(months)

        if '.' in str(days):
            days = float(days)
        else:
            days = int(days)

        if '.' in str(weeks):
            weeks = float(weeks)
        else:
            weeks = int(weeks)

        if '.' in str(hours):
            hours = float(hours)
        else:
            hours = int(hours)

        if '.' in str(minutes):
            minutes = float(minutes)
        else:
            minutes = int(minutes)

        if '.' in str(seconds):
            seconds = float(seconds)
        else:
            seconds = int(seconds)

        if '.' in str(microseconds):
            microseconds = float(microseconds)
        else:
            microseconds = int(microseconds)

        return dateutil.relativedelta.relativedelta(years=int(years), months=int(months), weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds, microseconds=microseconds)
