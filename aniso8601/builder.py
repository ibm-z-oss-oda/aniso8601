# -*- coding: utf-8 -*-

# Copyright (c) 2016, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime

from aniso8601.exceptions import DayOutOfBoundsError, \
        HoursOutOfBoundsError, ISOFormatError, LeapSecondError, \
        MidnightBoundsError, MinutesOutOfBoundsError, RelativeValueError, \
        SecondsOutOfBoundsError, WeekOutOfBoundsError, YearOutOfBoundsError

class BaseTimeBuilder(object):
    @classmethod
    def build_date(cls, YYYY=None, MM=None, DD=None, Www=None, D=None, DDD=None):
        raise NotImplementedError

    @classmethod
    def build_time(cls, hh=None, mm=None, ss=None, tz=None):
        raise NotImplementedError

    @classmethod
    def build_duration(cls, PnY=None, PnM=None, PnW=None, PnD=None, TnH=None, TnM=None, TnS=None):
        raise NotImplementedError

    @classmethod
    def build_timezone(cls, negative=None, Z=None, hh=None, mm=None, name=''):
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
    def build_date(cls, YYYY=None, MM=None, DD=None, Www=None, D=None, DDD=None):
        return (YYYY, MM, DD, Www, D, DDD)

    @classmethod
    def build_time(cls, hh=None, mm=None, ss=None, tz=None):
        return (hh, mm, ss, tz)

    @classmethod
    def build_duration(cls, PnY=None, PnM=None, PnW=None, PnD=None, TnH=None, TnM=None, TnS=None):
        return (PnY, PnM, PnW, PnD, TnH, TnM, TnS)

    @classmethod
    def build_timezone(cls, negative=None, Z=None, hh=None, mm=None, name=''):
        return (negative, Z, hh, mm, name)

    @classmethod
    def combine(cls, date, time):
        return (date, time)

class PythonTimeBuilder(BaseTimeBuilder):
    @classmethod
    def build_date(cls, YYYY=None, MM=None, DD=None, Www=None, D=None, DDD=None):
        if YYYY is not None:
            year = BaseTimeBuilder.cast(YYYY, int, thrownmessage='Invalid year string.')

        if MM is not None:
            month = BaseTimeBuilder.cast(MM, int, thrownmessage='Invalid month string.')
        else:
            month = 1

        if DD is not None:
            day = BaseTimeBuilder.cast(DD, int, thrownmessage='Invalid day string.')
        else:
            day = 1

        if Www is not None:
            weeknumber = BaseTimeBuilder.cast(Www, int, thrownmessage='Invalid week string.')
            if weeknumber == 0 or weeknumber > 53:
                raise WeekOutOfBoundsError('Week number must be between 1..53.')
        else:
            weeknumber = None

        if DDD is not None:
            dayofyear = BaseTimeBuilder.cast(DDD, int, thrownmessage='Invalid day string.')
        else:
            dayofyear = None

        if D is not None:
            dayofweek = BaseTimeBuilder.cast(D, int, thrownmessage='Invalid day string.')

            if dayofweek == 0 or dayofweek > 7:
                raise DayOutOfBoundsError('Weekday number must be between 1..7.')
        else:
            dayofweek = None

        #Range check
        if year == 0:
            raise YearOutOfBoundsError('Year must be between 1..9999.')

        if dayofyear is not None:
            return PythonTimeBuilder._build_ordinal_date(year, dayofyear)
        elif weeknumber is not None:
            return PythonTimeBuilder._build_week_date(year, weeknumber, isoday=dayofweek)

        return datetime.date(year, month, day)

    @classmethod
    def build_time(cls, hh=None, mm=None, ss=None, tz=None):
        #Builds a time from the given parts, handling fractional arguments where necessary
        hours = 0
        minutes = 0
        seconds = 0

        floathours = float(0)
        floatminutes = float(0)
        floatseconds = float(0)

        if hh is not None:
            if '.' in hh:
                floathours = BaseTimeBuilder.cast(hh, float, thrownmessage='Invalid hour string.')
                hours = 0
            else:
                hours = BaseTimeBuilder.cast(hh, int, thrownmessage='Invalid hour string.')

        if mm is not None:
            if '.' in mm:
                floatminutes = BaseTimeBuilder.cast(mm, float, thrownmessage='Invalid minute string.')
                minutes = 0
            else:
                minutes = BaseTimeBuilder.cast(mm, int, thrownmessage='Invalid minute string.')

        if ss is not None:
            if '.' in ss:
                #Truncate to maximum supported precision
                floatseconds = BaseTimeBuilder.cast(ss[0:ss.index('.') + 7], float, thrownmessage='Invalid second string.')
                seconds = 0
            else:
                seconds = BaseTimeBuilder.cast(ss, int, thrownmessage='Invalid second string.')

        #Range checks
        if hours == 23 and floathours == 0 and minutes == 59 and floatminutes == 0 and seconds == 60 and floatseconds == 0:
            #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
            raise LeapSecondError('Leap seconds are not supported.')

        if hours == 24 and floathours == 0 and (minutes != 0 or floatminutes != 0 or seconds != 0 or floatseconds != 0):
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
        result_datetime = datetime.datetime(1, 1, 1, hour=hours, minute=minutes, second=seconds, tzinfo=tz) + datetime.timedelta(hours=floathours, minutes=floatminutes, seconds=floatseconds)

        if tz is None:
            return result_datetime.time()

        return result_datetime.timetz()

    @classmethod
    def build_duration(cls, PnY=None, PnM=None, PnW=None, PnD=None, TnH=None, TnM=None, TnS=None):
        years = 0
        months = 0
        days = 0
        weeks = 0
        hours = 0
        minutes = 0
        seconds = 0

        if PnY is not None:
            years = BaseTimeBuilder.cast(PnY, float, thrownmessage='Invalid year string.')

        if PnM is not None:
            months = BaseTimeBuilder.cast(PnM, float, thrownmessage='Invalid month string.')
        if PnD is not None:
            days = BaseTimeBuilder.cast(PnD, float, thrownmessage='Invalid day string.')

        if PnW is not None:
            if '.' in PnW:
                weeks = BaseTimeBuilder.cast(PnW, float, thrownmessage='Invalid week string.')
            else:
                weeks = BaseTimeBuilder.cast(PnW, int, thrownmessage='Invalid week string.')

        if TnH is not None:
            if '.' in TnH:
                hours = BaseTimeBuilder.cast(TnH, float, thrownmessage='Invalid hour string.')
            else:
                hours = BaseTimeBuilder.cast(TnH, int, thrownmessage='Invalid hour string.')

        if TnM is not None:
            if '.' in TnM:
                minutes = BaseTimeBuilder.cast(TnM, float, thrownmessage='Invalid minute string.')
            else:
                minutes = BaseTimeBuilder.cast(TnM, int, thrownmessage='Invalid minute string.')

        if TnS is not None:
            if '.' in TnS:
                #Truncate to maximum supported precision
                seconds = BaseTimeBuilder.cast(TnS[0:TnS.index('.') + 7], float, thrownmessage='Invalid second string.')
            else:
                seconds = BaseTimeBuilder.cast(TnS, int, thrownmessage='Invalid second string.')

        #Note that weeks can be handled without conversion to days
        totaldays = years * 365 + months * 30 + days

        return datetime.timedelta(days=totaldays, seconds=seconds, minutes=minutes, hours=hours, weeks=weeks)

    @classmethod
    def build_timezone(cls, negative=None, Z=None, hh=None, mm=None, name=''):
        if Z is True:
            #Z -> UTC
            return UTCOffset(name='UTC', minutes=0)

        if hh is not None:
            tzhour = BaseTimeBuilder.cast(hh, int, thrownmessage='Invalid hour string.')
        else:
            tzhour = 0

        if mm is not None:
            tzminute = BaseTimeBuilder.cast(mm, int, thrownmessage='Invalid minute string.')
        else:
            tzminute = 0

        if negative is True:
            return UTCOffset(name=name, minutes=-(tzhour * 60 + tzminute))

        return UTCOffset(name=name, minutes=tzhour * 60 + tzminute)

    @classmethod
    def combine(cls, date, time):
        return datetime.datetime.combine(date, time)

    @staticmethod
    def _build_week_date(isoyear, isoweek, isoday=None):
        if isoday is None:
            return PythonTimeBuilder._iso_year_start(isoyear) + datetime.timedelta(weeks=isoweek - 1)

        return PythonTimeBuilder._iso_year_start(isoyear) + datetime.timedelta(weeks=isoweek - 1, days=isoday - 1)

    @staticmethod
    def _build_ordinal_date(isoyear, isoday):
        #Day of year to a date
        #https://stackoverflow.com/questions/2427555/python-question-year-and-day-of-year-to-date
        builtdate = datetime.date(isoyear, 1, 1) + datetime.timedelta(days=isoday - 1)

        #Enforce ordinal day limitation
        #https://bitbucket.org/nielsenb/aniso8601/issues/14/parsing-ordinal-dates-should-only-allow
        if isoday == 0 or builtdate.year != isoyear:
            raise DayOutOfBoundsError('Day of year must be from 1..365, 1..366 for leap year.')

        return builtdate

    @staticmethod
    def _iso_year_start(isoyear):
        #Given an ISO year, returns the equivalent of the start of the year
        #on the Gregorian calendar (which is used by Python)
        #Stolen from:
        #http://stackoverflow.com/questions/304256/whats-the-best-way-to-find-the-inverse-of-datetime-isocalendar

        #Determine the location of the 4th of January, the first week of
        #the ISO year is the week containing the 4th of January
        #http://en.wikipedia.org/wiki/ISO_week_date
        fourth_jan = datetime.date(isoyear, 1, 4)

        #Note the conversion from ISO day (1 - 7) and Python day (0 - 6)
        delta = datetime.timedelta(days=fourth_jan.isoweekday() - 1)

        #Return the start of the year
        return fourth_jan - delta

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

class UTCOffset(datetime.tzinfo):
    def __init__(self, name=None, minutes=None):
        #We build an offset in this manner since the
        #tzinfo class must have an init
        #"method that can be called with no arguments"
        self._name = name

        if minutes is not None:
            self._utcdelta = datetime.timedelta(minutes=minutes)
        else:
            self._utcdelta = None

    def __repr__(self):
        if self._utcdelta >= datetime.timedelta(hours=0):
            return '+{0} UTC'.format(self._utcdelta)

        #From the docs:
        #String representations of timedelta objects are normalized
        #similarly to their internal representation. This leads to
        #somewhat unusual results for negative timedeltas.

        #Clean this up for printing purposes
        correcteddays = abs(self._utcdelta.days + 1) #Negative deltas start at -1 day

        deltaseconds = (24 * 60 * 60) - self._utcdelta.seconds #Negative deltas have a positive seconds

        days, remainder = divmod(deltaseconds, 24 * 60 * 60) #(24 hours / day) * (60 minutes / hour) * (60 seconds / hour)
        hours, remainder = divmod(remainder, 1 * 60 * 60) #(1 hour) * (60 minutes / hour) * (60 seconds / hour)
        minutes, seconds = divmod(remainder, 1 * 60) #(1 minute) * (60 seconds / minute)

        #Add any remaining days to the correctedDays count
        correcteddays += days

        if correcteddays == 0:
            return '-{0}:{1:02}:{2:02} UTC'.format(hours, minutes, seconds)
        elif correcteddays == 1:
            return '-1 day, {0}:{1:02}:{2:02} UTC'.format(hours, minutes, seconds)

        return '-{0} days, {1}:{2:02}:{3:02} UTC'.format(correcteddays, hours, minutes, seconds)

    def utcoffset(self, dt):
        return self._utcdelta

    def tzname(self, dt):
        return self._name

    def dst(self, dt):
        #ISO 8601 specifies offsets should be different if DST is required,
        #instead of allowing for a DST to be specified
        # https://docs.python.org/2/library/datetime.html#datetime.tzinfo.dst
        return datetime.timedelta(0)
