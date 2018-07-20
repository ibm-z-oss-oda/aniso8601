# -*- coding: utf-8 -*-

# Copyright (c) 2016, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime

from aniso8601.exceptions import HoursOutOfBoundsError, ISOFormatError, \
        LeapSecondError, MidnightBoundsError, MinutesOutOfBoundsError, \
        RelativeValueError, SecondsOutOfBoundsError, YearOutOfBoundsError

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

    @staticmethod
    def cast(value, castfunction, caughtexceptions=(ValueError,), thrownexception=ISOFormatError, thrownmessage=None):
        try:
            result = castfunction(value)
        except caughtexceptions:
            raise thrownexception(thrownmessage)

        return result

class NoneBuilder(BaseTimeBuilder):
    #Builder used to return the arguments, helps clean up some parse methods
    @classmethod
    def build_date(cls, year, month, day):
        return (year, month, day)

    @classmethod
    def build_time(cls, hours=0, minutes=0, seconds=0, microseconds=0, tzinfo=None):
        return (hours, minutes, seconds, microseconds, tzinfo)

    @classmethod
    def build_datetime(cls, year, month, day, hours=0, minutes=0, seconds=0, microseconds=0, tzinfo=None):
        return (year, month, day, hours, minutes, seconds, microseconds, tzinfo)

    @classmethod
    def build_timedelta(cls, years=0, months=0, days=0, weeks=0, hours=0, minutes=0, seconds=0, microseconds=0):
        return (years, months, days, weeks, hours, minutes, seconds, microseconds)

class PythonTimeBuilder(BaseTimeBuilder):
    @classmethod
    def build_date(cls, year, month, day):
        year = BaseTimeBuilder.cast(year, int, thrownmessage='Invalid year string.')
        month = BaseTimeBuilder.cast(month, int, thrownmessage='Invalid month string.')
        day = BaseTimeBuilder.cast(day, int, thrownmessage='Invalid day string.')

        #Range check
        if year == 0:
            raise YearOutOfBoundsError('Year must be between 1..9999.')

        return datetime.date(year, month, day)

    @classmethod
    def build_time(cls, hours=0, minutes=0, seconds=0, microseconds=0, tzinfo=None):
        #Builds a time from the given parts, handling fractional arguments where necessary
        floathours = float(0)
        floatminutes = float(0)
        floatseconds = float(0)

        if '.' in str(hours):
            floathours = BaseTimeBuilder.cast(hours, float, thrownmessage='Invalid hour string.')
            hours = 0
        else:
            hours = BaseTimeBuilder.cast(hours, int, thrownmessage='Invalid hour string.')

        if '.' in str(minutes):
            floatminutes = BaseTimeBuilder.cast(minutes, float, thrownmessage='Invalid minute string.')
            minutes = 0
        else:
            minutes = BaseTimeBuilder.cast(minutes, int, thrownmessage='Invalid minute string.')

        if '.' in str(seconds):
            floatseconds = BaseTimeBuilder.cast(seconds, float, thrownmessage='Invalid second string.')
            seconds = 0
        else:
            seconds = BaseTimeBuilder.cast(seconds, int, thrownmessage='Invalid second string.')

        #No fractional microseconds
        microseconds = BaseTimeBuilder.cast(microseconds, int, thrownmessage='Invalid microsecond string.')

        #Range checks
        if hours == 23 and floathours == 0 and minutes == 59 and floatminutes == 0 and seconds == 60 and floatseconds == 0:
            #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
            raise LeapSecondError('Leap seconds are not supported.')

        if hours == 24 and floathours == 0 and (minutes != 0 or floatminutes != 0 or seconds != 0 or floatseconds != 0 or microseconds != 0):
            raise MidnightBoundsError('Hour 24 may only represent midnight.')

        if hours > 24 or floathours > 24:
            raise HoursOutOfBoundsError('Hour must be between 0..24 with 24 representing midnight.')

        if minutes >= 60 or floatminutes >= 60:
            raise MinutesOutOfBoundsError('Minutes must be less than 60.')

        if seconds >= 60 or floatseconds >= 60:
            raise SecondsOutOfBoundsError('Seconds must be less than 60.')

        #Fix ranges that have passed range checks
        if hours == 24:
            hours = 0
            minutes = 0
            seconds = 0

        #Datetimes don't handle fractional components, so we use a timedelta
        result_datetime = datetime.datetime(1, 1, 1, hour=hours, minute=minutes, second=seconds, microsecond=microseconds, tzinfo=tzinfo) + cls.build_timedelta(hours=floathours, minutes=floatminutes, seconds=floatseconds)

        if tzinfo is None:
            return result_datetime.time()

        return result_datetime.timetz()

    @classmethod
    def build_datetime(cls, year, month, day, hours=0, minutes=0, seconds=0, microseconds=0, tzinfo=None):
        #Builds a datetime from the given parts, handling fractional arguments where necessary
        date = cls.build_date(year, month, day)
        time = cls.build_time(hours=hours, minutes=minutes, seconds=seconds, microseconds=microseconds, tzinfo=tzinfo)

        return cls.combine(date, time)

    @classmethod
    def build_timedelta(cls, years=0, months=0, days=0, weeks=0, hours=0, minutes=0, seconds=0, microseconds=0):
        years = BaseTimeBuilder.cast(years, float, thrownmessage='Invalid year string.')
        months = BaseTimeBuilder.cast(months, float, thrownmessage='Invalid month string.')
        days = BaseTimeBuilder.cast(days, float, thrownmessage='Invalid day string.')

        if '.' in str(weeks):
            weeks = BaseTimeBuilder.cast(weeks, float, thrownmessage='Invalid week string.')
        else:
            weeks = BaseTimeBuilder.cast(weeks, int, thrownmessage='Invalid week string.')

        if '.' in str(hours):
            hours = BaseTimeBuilder.cast(hours, float, thrownmessage='Invalid hour string.')
        else:
            hours = BaseTimeBuilder.cast(hours, int, thrownmessage='Invalid hour string.')

        if '.' in str(minutes):
            minutes = BaseTimeBuilder.cast(minutes, float, thrownmessage='Invalid minute string.')
        else:
            minutes = BaseTimeBuilder.cast(minutes, int, thrownmessage='Invalid minute string.')

        if '.' in str(seconds):
            #Truncate to maximum supported precision
            seconds = str(seconds)

            seconds = BaseTimeBuilder.cast(seconds[0:seconds.index('.') + 7], float, thrownmessage='Invalid second string.')
        else:
            seconds = BaseTimeBuilder.cast(seconds, int, thrownmessage='Invalid second string.')

        if '.' in str(microseconds):
            microseconds = BaseTimeBuilder.cast(microseconds, float, thrownmessage='Invalid microsecond string.')
        else:
            microseconds = BaseTimeBuilder.cast(microseconds, int, thrownmessage='Invalid microsecond string.')

        #Note that weeks can be handled without conversion to days
        totaldays = years * 365 + months * 30 + days

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

        if '.' in str(years) or '.' in str(months):
            #https://github.com/dateutil/dateutil/issues/40
            raise RelativeValueError('Fractional months and years are not defined for relative intervals.')

        years = BaseTimeBuilder.cast(years, int, thrownmessage='Invalid year string.')
        months = BaseTimeBuilder.cast(months, int, thrownmessage='Invalid month string.')

        if '.' in str(days):
            days = BaseTimeBuilder.cast(days, float, thrownmessage='Invalid day string.')
        else:
            days = BaseTimeBuilder.cast(days, int, thrownmessage='Invalid day string.')

        if '.' in str(weeks):
            weeks = BaseTimeBuilder.cast(weeks, float, thrownmessage='Invalid week string.')
        else:
            weeks = BaseTimeBuilder.cast(weeks, int, thrownmessage='Invalid week string.')

        if '.' in str(hours):
            hours = BaseTimeBuilder.cast(hours, float, thrownmessage='Invalid hour string.')
        else:
            hours = BaseTimeBuilder.cast(hours, int, thrownmessage='Invalid hour string.')

        if '.' in str(minutes):
            minutes = BaseTimeBuilder.cast(minutes, float, thrownmessage='Invalid minute string.')
        else:
            minutes = BaseTimeBuilder.cast(minutes, int, thrownmessage='Invalid minute string.')

        if '.' in str(seconds):
            #Truncate to maximum supported precision
            seconds, secondsremainder = str(seconds).split('.')

            seconds = BaseTimeBuilder.cast(seconds, int, thrownmessage='Invalid second string.')

            secondsremainder = BaseTimeBuilder.cast('.' + secondsremainder[0:6], float, thrownmessage='Invalid second string.')
        else:
            seconds = seconds = BaseTimeBuilder.cast(seconds, int, thrownmessage='Invalid second string.')
            secondsremainder = 0

        if '.' in str(microseconds):
            microseconds = BaseTimeBuilder.cast(microseconds, float, thrownmessage='Invalid microsecond string.')
        else:
            microseconds = BaseTimeBuilder.cast(microseconds, int, thrownmessage='Invalid microsecond string.')

        microseconds += secondsremainder * 1e6 #Add remaining microseconds

        return dateutil.relativedelta.relativedelta(years=years, months=months, weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds, microseconds=microseconds)
