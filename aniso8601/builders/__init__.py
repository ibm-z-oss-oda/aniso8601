# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import calendar

from aniso8601.exceptions import (DayOutOfBoundsError, MidnightBoundsError,
                                  MinutesOutOfBoundsError, MonthOutOfBoundsError,
                                  NegativeDurationError, HoursOutOfBoundsError,
                                  ISOFormatError, LeapSecondError,
                                  SecondsOutOfBoundsError, WeekOutOfBoundsError,
                                  YearOutOfBoundsError)
from collections import namedtuple

DateTuple = namedtuple('Date', ['YYYY', 'MM', 'DD', 'Www', 'D', 'DDD'])
TimeTuple = namedtuple('Time', ['hh', 'mm', 'ss', 'tz'])
DatetimeTuple = namedtuple('Datetime', ['date', 'time'])
DurationTuple = namedtuple('Duration', ['PnY', 'PnM', 'PnW', 'PnD',
                                        'TnH', 'TnM', 'TnS'])
IntervalTuple = namedtuple('Interval', ['start', 'end', 'duration'])
RepeatingIntervalTuple = namedtuple('RepeatingInterval', ['R', 'Rnn',
                                                          'interval'])
TimezoneTuple = namedtuple('Timezone', ['negative', 'Z', 'hh', 'mm', 'name'])

Limit = namedtuple('Limit', ['casterrorstring', 'min', 'max',
                             'rangeexception', 'rangeerrorstring'])

class BaseTimeBuilder(object):
    #Limit tuple format cast function, cast error string,
    #lower limit, upper limit, limit error string
    DATE_YYYY_LIMIT = Limit('Invalid year string.',
                            0000, 9999, YearOutOfBoundsError,
                            'Year must be between 1..9999.')
    DATE_MM_LIMIT = Limit('Invalid month string.',
                          1, 12, MonthOutOfBoundsError,
                          'Month must be between 1..12.')
    DATE_DD_LIMIT = Limit('Invalid day string.',
                          1, 31, DayOutOfBoundsError,
                          'Day must be between 1..31.')
    DATE_WWW_LIMIT = Limit('Invalid week string.',
                           1, 53, WeekOutOfBoundsError,
                           'Week number must be between 1..53.')
    DATE_D_LIMIT = Limit('Invalid weekday string.',
                         1, 7, DayOutOfBoundsError,
                         'Weekday number must be between 1..7.')
    DATE_DDD_LIMIT = Limit('Invalid ordinal day string.',
                           1, 366, DayOutOfBoundsError,
                           'Ordinal day must be between 1..366.')
    TIME_HH_LIMIT = Limit('Invalid hour string.',
                          0, 24, HoursOutOfBoundsError,
                          'Hour must be between 0..24 with '
                          '24 representing midnight.')
    TIME_MM_LIMIT = Limit('Invalid minute string.',
                          0, 59, MinutesOutOfBoundsError,
                          'Minute must be between 0..59.')
    TIME_SS_LIMIT = Limit('Invalid second string.',
                          0, 60, SecondsOutOfBoundsError,
                          'Second must be between 0..60 with '
                          '60 representing a leap second.')
    TZ_HH_LIMIT = Limit('Invalid timezone hour string.',
                        0, 23, HoursOutOfBoundsError,
                        'Hour must be between 0..23.')
    TZ_MM_LIMIT = Limit('Invalid timezone minute string.',
                        0, 59, MinutesOutOfBoundsError,
                        'Minute must be between 0..59.')
    DURATION_PNY_LIMIT = Limit('Invalid year duration string.',
                               None, None, YearOutOfBoundsError,
                               None)
    DURATION_PNM_LIMIT = Limit('Invalid month duration string.',
                               None, None, MonthOutOfBoundsError,
                               None)
    DURATION_PNW_LIMIT = Limit('Invalid week duration string.',
                               None, None, WeekOutOfBoundsError,
                               None)
    DURATION_PND_LIMIT = Limit('Invalid day duration string.',
                               None, None, DayOutOfBoundsError,
                               None)
    DURATION_TNH_LIMIT = Limit('Invalid hour duration string.',
                               None, None, HoursOutOfBoundsError,
                               None)
    DURATION_TNM_LIMIT = Limit('Invalid minute duration string.',
                               None, None, MinutesOutOfBoundsError,
                               None)
    DURATION_TNS_LIMIT = Limit('Invalid second duration string.',
                               None, None, SecondsOutOfBoundsError,
                               None)
    INTERVAL_RNN_LIMIT = Limit('Invalid duration repetition string.',
                               0, None, NegativeDurationError,
                               'Duration repetition count must be positive.')

    LEAP_SECONDS_SUPPORTED = False

    @classmethod
    def build_date(cls, YYYY=None, MM=None, DD=None, Www=None, D=None,
                   DDD=None):
        raise NotImplementedError

    @classmethod
    def build_time(cls, hh=None, mm=None, ss=None, tz=None):
        raise NotImplementedError

    @classmethod
    def build_datetime(cls, date, time):
        raise NotImplementedError

    @classmethod
    def build_duration(cls, PnY=None, PnM=None, PnW=None, PnD=None, TnH=None,
                       TnM=None, TnS=None):
        raise NotImplementedError

    @classmethod
    def build_interval(cls, start=None, end=None, duration=None):
        #start, end, and duration are all tuples
        raise NotImplementedError

    @classmethod
    def build_repeating_interval(cls, R=None, Rnn=None, interval=None):
        #interval is a tuple
        raise NotImplementedError

    @classmethod
    def build_timezone(cls, negative=None, Z=None, hh=None, mm=None, name=''):
        raise NotImplementedError

    @classmethod
    def range_check_date(cls, YYYY=None, MM=None, DD=None,
                         Www=None, D=None, DDD=None):

        if YYYY is not None:
            YYYYvalue = cls._range_check(YYYY, cls.DATE_YYYY_LIMIT)

        if MM is not None:
            MMvalue = cls._range_check(MM, cls.DATE_MM_LIMIT)

        if DD is not None:
            DDvalue = cls._range_check(DD, cls.DATE_DD_LIMIT)

            #Check calendar
            if DDvalue > calendar.monthrange(YYYYvalue, MMvalue)[1]:
                raise DayOutOfBoundsError('{0} is out of range for {1}-{2}'.format(DD, YYYY, MM))

        if Www is not None:
            cls._range_check(Www, cls.DATE_WWW_LIMIT)

        if D is not None:
            cls._range_check(D, cls.DATE_D_LIMIT)

        if DDD is not None:
            DDDvalue = cls._range_check(DDD, cls.DATE_DDD_LIMIT)

            if calendar.isleap(YYYYvalue) is False and DDDvalue >= 366:
                raise DayOutOfBoundsError('{0} is only valid for leap year.'.format(DDD))

    @classmethod
    def range_check_time(cls, hh=None, mm=None, ss=None):
        #Used for leap second handling
        hhvalue = None
        mmvalue = None
        ssvalue = None

        midnight = False #Handle hh = '24' specially

        if hh is not None:
            if hh[0:2] == '24':
                if '.' in hh[2:]:
                    raise MidnightBoundsError('Hour 24 may only represent midnight.')

                midnight = True

            hhvalue = cls._range_check(hh, cls.TIME_HH_LIMIT)

        if mm is not None:
            mmvalue = cls._range_check(mm, cls.TIME_MM_LIMIT)

        if ss is not None:
            ssvalue = cls._range_check(ss, cls.TIME_SS_LIMIT)

        #Handle midnight range
        if midnight is True and ((mmvalue is not None and mmvalue != 0) or (ssvalue is not None and ssvalue != 0)):
            raise MidnightBoundsError('Hour 24 may only represent midnight.')

        if cls.LEAP_SECONDS_SUPPORTED is True:
            if hhvalue != 23 and mmvalue != 59 and ssvalue == 60:
                raise cls.TIME_SS_LIMIT.rangeexception(cls.TIME_SS_LIMIT.rangeerrorstring)
        else:
            if hhvalue == 23 and mmvalue == 59 and ssvalue == 60:
                #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
                raise LeapSecondError('Leap seconds are not supported.')

            if ssvalue == 60:
                raise cls.TIME_SS_LIMIT.rangeexception(cls.TIME_SS_LIMIT.rangeerrorstring)

    @classmethod
    def range_check_duration(cls, PnY=None, PnM=None, PnW=None, PnD=None,
                             TnH=None, TnM=None, TnS=None):
        if PnY is not None:
            cls._range_check(PnY, cls.DURATION_PNY_LIMIT)

        if PnM is not None:
            cls._range_check(PnM, cls.DURATION_PNM_LIMIT)

        if PnW is not None:
            cls._range_check(PnW, cls.DURATION_PNW_LIMIT)

        if PnD is not None:
            cls._range_check(PnD, cls.DURATION_PND_LIMIT)

        if TnH is not None:
            cls._range_check(TnH, cls.DURATION_TNH_LIMIT)

        if TnM is not None:
            cls._range_check(TnM, cls.DURATION_TNM_LIMIT)

        if TnS is not None:
            cls._range_check(TnS, cls.DURATION_TNS_LIMIT)

    @classmethod
    def range_check_repeating_interval(cls, Rnn=None):
        if Rnn is not None:
            cls._range_check(Rnn, cls.INTERVAL_RNN_LIMIT)

    @classmethod
    def range_check_timezone(cls, negative=None, hh=None, mm=None):
        if hh is not None:
            hhvalue = cls._range_check(hh, cls.TZ_HH_LIMIT)

            if mm is not None:
                mmvalue = cls._range_check(mm, cls.TZ_MM_LIMIT)
            else:
                mmvalue = 0

            if negative is True:
                if hhvalue == 0 and mmvalue == 0:
                    raise ISOFormatError('Negative ISO 8601 time offset must not '
                                         'be 0.')

    @classmethod
    def _range_check(cls, valuestr, limit):
        #Returns casted value if in range, raises defined exceptions on failure

        if '.' in valuestr:
            castfunc = float
        else:
            castfunc = int

        value = BaseTimeBuilder.cast(valuestr, castfunc, thrownmessage=limit.casterrorstring)

        if limit.min is not None and value < limit.min:
            raise limit.rangeexception(limit.rangeerrorstring)

        if limit.max is not None and value > limit.max:
            raise limit.rangeexception(limit.rangeerrorstring)

        return value

    @staticmethod
    def cast(value, castfunction, caughtexceptions=(ValueError,),
             thrownexception=ISOFormatError, thrownmessage=None):

        try:
            result = castfunction(value)
        except caughtexceptions:
            raise thrownexception(thrownmessage)

        return result

    @classmethod
    def _build_object(cls, parsetuple):
        #Given a TupleBuilder tuple, build the correct object
        if type(parsetuple) is DateTuple:
            return cls.build_date(YYYY=parsetuple.YYYY, MM=parsetuple.MM,
                                  DD=parsetuple.DD, Www=parsetuple.Www,
                                  D=parsetuple.D, DDD=parsetuple.DDD)

        if type(parsetuple) is TimeTuple:
            return cls.build_time(hh=parsetuple.hh, mm=parsetuple.mm,
                                  ss=parsetuple.ss, tz=parsetuple.tz)

        if type(parsetuple) is DatetimeTuple:
            return cls.build_datetime(parsetuple.date, parsetuple.time)

        if type(parsetuple) is DurationTuple:
            return cls.build_duration(PnY=parsetuple.PnY, PnM=parsetuple.PnM,
                                      PnW=parsetuple.PnW, PnD=parsetuple.PnD,
                                      TnH=parsetuple.TnH, TnM=parsetuple.TnM,
                                      TnS=parsetuple.TnS)

        if type(parsetuple) is IntervalTuple:
            return cls.build_interval(start=parsetuple.start, end=parsetuple.end,
                                      duration=parsetuple.duration)

        if type(parsetuple) is RepeatingIntervalTuple:
            return cls.build_repeating_interval(R=parsetuple.R,
                                                Rnn=parsetuple.Rnn,
                                                interval=parsetuple.interval)

        return cls.build_timezone(negative=parsetuple.negative, Z=parsetuple.Z,
                                  hh=parsetuple.hh, mm=parsetuple.mm,
                                  name=parsetuple.name)

class TupleBuilder(BaseTimeBuilder):
    #Builder used to return the arguments as a tuple, cleans up some parse methods
    @classmethod
    def build_date(cls, YYYY=None, MM=None, DD=None, Www=None, D=None,
                   DDD=None):

        return DateTuple(YYYY, MM, DD, Www, D, DDD)

    @classmethod
    def build_time(cls, hh=None, mm=None, ss=None, tz=None):
        return TimeTuple(hh, mm, ss, tz)

    @classmethod
    def build_datetime(cls, date, time):
        return DatetimeTuple(date, time)

    @classmethod
    def build_duration(cls, PnY=None, PnM=None, PnW=None, PnD=None, TnH=None,
                       TnM=None, TnS=None):

        return DurationTuple(PnY, PnM, PnW, PnD, TnH, TnM, TnS)

    @classmethod
    def build_interval(cls, start=None, end=None, duration=None):
        return IntervalTuple(start, end, duration)

    @classmethod
    def build_repeating_interval(cls, R=None, Rnn=None, interval=None):
        return RepeatingIntervalTuple(R, Rnn, interval)

    @classmethod
    def build_timezone(cls, negative=None, Z=None, hh=None, mm=None, name=''):
        return TimezoneTuple(negative, Z, hh, mm, name)

def range_check_date(build_method):
    """
    Range check decorator for build_date
    """
    def peform_range_check(cls, *args, **kwargs):
        cls.range_check_date(**kwargs)
        return build_method(cls, *args, **kwargs)

    return peform_range_check

def range_check_time(build_method):
    """
    Range check decorator for build_time
    """
    def peform_range_check(cls, *args, **kwargs):
        #Filter out timezone, it's checked separate
        filteredkwargs = _filter_kwargs(kwargs, ['tz'])

        cls.range_check_time(**filteredkwargs)
        return build_method(cls, *args, **kwargs)

    return peform_range_check

def range_check_duration(build_method):
    """
    Range check decorator for build_duration
    """
    def peform_range_check(cls, *args, **kwargs):
        cls.range_check_duration(**kwargs)
        return build_method(cls, *args, **kwargs)

    return peform_range_check

def range_check_repeating_interval(build_method):
    """
    Range check decorator for build_repeating_interval
    """
    def peform_range_check(cls, *args, **kwargs):
        filteredkwargs = _filter_kwargs(kwargs, ['R', 'interval'])

        cls.range_check_repeating_interval(**filteredkwargs)
        return build_method(cls, *args, **kwargs)

    return peform_range_check

def range_check_timezone(build_method):
    """
    Range check decorator for build_timezone
    """
    def peform_range_check(cls, *args, **kwargs):
        filteredkwargs = _filter_kwargs(kwargs, ['Z', 'name'])

        cls.range_check_timezone(**filteredkwargs)
        return build_method(cls, *args, **kwargs)

    return peform_range_check

def _filter_kwargs(tofilter, excludedkeys):
    filteredkwargs = {}

    for key in tofilter:
        if key not in excludedkeys:
            filteredkwargs[key] = tofilter[key]

    return filteredkwargs
