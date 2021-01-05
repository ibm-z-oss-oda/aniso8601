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

class BaseTimeBuilder(object):
    #Constants
    CAST_FUNCTION_IDX = 0
    CAST_ERROR_STRING_IDX = 1
    RANGE_MIN_IDX = 2
    RANGE_MAX_IDX = 3
    OUT_OF_RANGE_EXCEPTION_IDX = 4
    OUT_OF_RANGE_ERROR_STRING_IDX = 5

    #Limit tuple format cast function, cast error string,
    #lower limit, upper limit, limit error string
    DATE_YYYY_LIMITS = ((int,), 'Invalid year string.',
                        0000, 9999, YearOutOfBoundsError,
                        'Year must be between 1..9999.')
    DATE_MM_LIMITS = ((int,), 'Invalid month string.',
                      1, 12, MonthOutOfBoundsError,
                      'Month must be between 1..12.')
    DATE_DD_LIMITS = ((int,), 'Invalid day string.',
                      1, 31, DayOutOfBoundsError,
                      'Day must be between 1..31.')
    DATE_WWW_LIMITS = ((int,), 'Invalid week string.',
                       1, 53, WeekOutOfBoundsError,
                       'Week number must be between 1..53.')
    DATE_D_LIMITS = ((int,), 'Invalid weekday string.',
                     1, 7, DayOutOfBoundsError,
                     'Weekday number must be between 1..7.')
    DATE_DDD_LIMITS = ((int,), 'Invalid ordinal day string.',
                       1, 366, DayOutOfBoundsError,
                       'Ordinal day must be between 1..366.')
    TIME_HH_LIMITS = ((float, int), 'Invalid hour string.',
                      0, 24, HoursOutOfBoundsError,
                      'Hour must be between 0..24 with '
                      '24 representing midnight.')
    TIME_MM_LIMITS = ((float, int), 'Invalid minute string.',
                      0, 59, MinutesOutOfBoundsError,
                      'Minute must be between 0..59.')
    TIME_SS_LIMITS = ((float, int), 'Invalid second string.',
                      0, 60, SecondsOutOfBoundsError,
                      'Second must be between 0..60 with '
                      '60 representing a leap second.')
    TZ_HH_LIMITS = ((int,), 'Invalid timezone hour string.',
                    0, 23, HoursOutOfBoundsError,
                    'Hour must be between 0..23.')
    TZ_MM_LIMITS = ((int,), 'Invalid timezone minute string.',
                    0, 59, MinutesOutOfBoundsError,
                    'Minute must be between 0..59.')
    DURATION_PNY_LIMITS = ((float, int), 'Invalid year duration string.',
                           None, None, None,
                           None)
    DURATION_PNM_LIMITS = ((float, int), 'Invalid month duration string.',
                           None, None, None,
                           None)
    DURATION_PNW_LIMITS = ((float, int), 'Invalid week duration string.',
                           None, None, None,
                           None)
    DURATION_PND_LIMITS = ((float, int), 'Invalid day duration string.',
                           None, None, None,
                           None)
    DURATION_TNH_LIMITS = ((float, int), 'Invalid hour duration string.',
                           None, None, None,
                           None)
    DURATION_TNM_LIMITS = ((float, int), 'Invalid minute duration string.',
                           None, None, None,
                           None)
    DURATION_TNS_LIMITS = ((float, int), 'Invalid second duration string.',
                           None, None, None,
                           None)
    INTERVAL_RNN_LIMITS = ((int,), 'Invalid duration repetition string.',
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
            YYYYvalue = cls._range_check(YYYY, cls.DATE_YYYY_LIMITS)

        if MM is not None:
            MMvalue = cls._range_check(MM, cls.DATE_MM_LIMITS)

        if DD is not None:
            DDvalue = cls._range_check(DD, cls.DATE_DD_LIMITS)

            #Check calendar
            if DDvalue > calendar.monthrange(YYYYvalue, MMvalue)[1]:
                raise DayOutOfBoundsError('{0} is out of range for {1}-{2}'.format(DD, YYYY, MM))

        if Www is not None:
            cls._range_check(Www, cls.DATE_WWW_LIMITS)

        if D is not None:
            cls._range_check(D, cls.DATE_D_LIMITS)

        if DDD is not None:
            DDDvalue = cls._range_check(DDD, cls.DATE_DDD_LIMITS)

            if calendar.isleap(YYYYvalue) is False and DDDvalue >= 366:
                raise DayOutOfBoundsError('{0} is only valid for leap year.'.format(DDD))

    @classmethod
    def range_check_time(cls, hh=None, mm=None, ss=None):
        #Used for leap second handling
        hhvalue = None
        mmvalue = None
        ssvalue = None

        midnight = False #Handle hh = '24' specially
        fractionalcomponent = False #Only one fractional component allowed

        if hh is not None:
            if hh[0:2] == '24':
                if '.' in hh[2:]:
                    raise MidnightBoundsError('Hour 24 may only represent midnight.')

                midnight = True

            hhvalue = cls._range_check(hh, cls.TIME_HH_LIMITS)

            fractionalcomponent = hhvalue is float

        if mm is not None:
            mmvalue = cls._range_check(mm, cls.TIME_MM_LIMITS)

            if fractionalcomponent is True and mmvalue is float:
                raise ISOFormatError('Only one fractional component allowed.')

            fractionalcomponent = mmvalue is float

        if ss is not None:
            ssvalue = cls._range_check(ss, cls.TIME_SS_LIMITS)

            if fractionalcomponent is True and ssvalue is float:
                raise ISOFormatError('Only one fractional component allowed.')

            fractionalcomponent = ssvalue is float

        #Handle midnight range
        if midnight is True and ((mmvalue is not None and mmvalue != 0) or (ssvalue is not None and ssvalue != 0)):
            raise MidnightBoundsError('Hour 24 may only represent midnight.')

        if cls.LEAP_SECONDS_SUPPORTED is True:
            if hhvalue != 23 and mmvalue != 59 and ssvalue == 60:
                raise cls.TIME_SS_LIMITS[cls.OUT_OF_RANGE_EXCEPTION_IDX](cls.TIME_SS_LIMITS[cls.OUT_OF_RANGE_ERROR_STRING_IDX])
        else:
            if hhvalue == 23 and mmvalue == 59 and ssvalue == 60:
                #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
                raise LeapSecondError('Leap seconds are not supported.')

            if ssvalue == 60:
                raise cls.TIME_SS_LIMITS[cls.OUT_OF_RANGE_EXCEPTION_IDX](cls.TIME_SS_LIMITS[cls.OUT_OF_RANGE_ERROR_STRING_IDX])

    @classmethod
    def range_check_duration(cls, PnY=None, PnM=None, PnW=None, PnD=None,
                             TnH=None, TnM=None, TnS=None, Rnn=None):
        fractionalcomponent = False #Only one fractional component allowed

        if PnY is not None:
            result = cls._range_check(PnY, cls.DURATION_PNY_LIMITS)

            fractionalcomponent = result is float

        if PnM is not None:
            result = cls._range_check(PnM, cls.DURATION_PNM_LIMITS)

            if fractionalcomponent is True and result is float:
                raise ISOFormatError('Only one fractional component allowed.')

            fractionalcomponent = result is float

        if PnW is not None:
            result = cls._range_check(PnW, cls.DURATION_PNW_LIMITS)

            if fractionalcomponent is True and result is float:
                raise ISOFormatError('Only one fractional component allowed.')

            fractionalcomponent = result is float

        if PnD is not None:
            result = cls._range_check(PnD, cls.DURATION_PND_LIMITS)

            if fractionalcomponent is True and result is float:
                raise ISOFormatError('Only one fractional component allowed.')

            fractionalcomponent = result is float

        if TnH is not None:
            result = cls._range_check(TnH, cls.DURATION_TNH_LIMITS)

            if fractionalcomponent is True and result is float:
                raise ISOFormatError('Only one fractional component allowed.')

            fractionalcomponent = result is float

        if TnM is not None:
            result = cls._range_check(TnM, cls.DURATION_TNM_LIMITS)

            if fractionalcomponent is True and result is float:
                raise ISOFormatError('Only one fractional component allowed.')

            fractionalcomponent = result is float

        if TnS is not None:
            result = cls._range_check(TnS, cls.DURATION_TNS_LIMITS)

            if fractionalcomponent is True and result is float:
                raise ISOFormatError('Only one fractional component allowed.')

    @classmethod
    def range_check_repeating_interval(cls, Rnn=None):
        if Rnn is not None:
            cls._range_check(Rnn, cls.INTERVAL_RNN_LIMITS)

    @classmethod
    def range_check_timezone(cls, negative=None, hh=None, mm=None):
        if hh is not None:
            hhvalue = cls._range_check(hh, cls.TZ_HH_LIMITS)

            if mm is not None:
                mmvalue = cls._range_check(mm, cls.TZ_MM_LIMITS)
            else:
                mmvalue = 0

            if negative is True:
                if hhvalue == 0 and mmvalue == 0:
                    raise ISOFormatError('Negative ISO 8601 time offset must not '
                                         'be 0.')

    @classmethod
    def _range_check(cls, valuestr, rangetuple):
        #Returns casted value if in range, raises defined exceptions on failure
        castfuncs = rangetuple[cls.CAST_FUNCTION_IDX]
        casterrorstring = rangetuple[cls.CAST_ERROR_STRING_IDX]
        rangemin = rangetuple[cls.RANGE_MIN_IDX]
        rangemax = rangetuple[cls.RANGE_MAX_IDX]
        rangeexception = rangetuple[cls.OUT_OF_RANGE_EXCEPTION_IDX]
        rangeerrorstring = rangetuple[cls.OUT_OF_RANGE_ERROR_STRING_IDX]

        if '.' in valuestr:
            if float not in castfuncs:
                raise ISOFormatError(casterrorstring)

            castfunc = float
            fractionalcomponent = True
        else:
            castfunc = int

        value = BaseTimeBuilder.cast(valuestr, castfunc, thrownmessage=casterrorstring)

        if rangemin is not None:
            if value < rangemin:
                raise rangeexception(rangeerrorstring)

        if rangemax is not None:
            if value > rangemax:
                raise rangeexception(rangeerrorstring)

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
        if parsetuple[-1] == 'date':
            return cls.build_date(YYYY=parsetuple[0], MM=parsetuple[1],
                                  DD=parsetuple[2], Www=parsetuple[3],
                                  D=parsetuple[4], DDD=parsetuple[5])
        elif parsetuple[-1] == 'time':
            return cls.build_time(hh=parsetuple[0], mm=parsetuple[1],
                                  ss=parsetuple[2], tz=parsetuple[3])
        elif parsetuple[-1] == 'datetime':
            return cls.build_datetime(parsetuple[0], parsetuple[1])
        elif parsetuple[-1] == 'duration':
            return cls.build_duration(PnY=parsetuple[0], PnM=parsetuple[1],
                                      PnW=parsetuple[2], PnD=parsetuple[3],
                                      TnH=parsetuple[4], TnM=parsetuple[5],
                                      TnS=parsetuple[6])
        elif parsetuple[-1] == 'interval':
            return cls.build_interval(start=parsetuple[0], end=parsetuple[1],
                                      duration=parsetuple[2])
        elif parsetuple[-1] == 'repeatinginterval':
            return cls.build_repeating_interval(R=parsetuple[0],
                                                Rnn=parsetuple[1],
                                                interval=parsetuple[2])

        return cls.build_timezone(negative=parsetuple[0], Z=parsetuple[1],
                                  hh=parsetuple[2], mm=parsetuple[3],
                                  name=parsetuple[4])

class TupleBuilder(BaseTimeBuilder):
    #Builder used to return the arguments as a tuple, cleans up some parse methods
    @classmethod
    def build_date(cls, YYYY=None, MM=None, DD=None, Www=None, D=None,
                   DDD=None):

        return (YYYY, MM, DD, Www, D, DDD, 'date')

    @classmethod
    def build_time(cls, hh=None, mm=None, ss=None, tz=None):
        return (hh, mm, ss, tz, 'time')

    @classmethod
    def build_datetime(cls, date, time):
        return (date, time, 'datetime')

    @classmethod
    def build_duration(cls, PnY=None, PnM=None, PnW=None, PnD=None, TnH=None,
                       TnM=None, TnS=None):

        return (PnY, PnM, PnW, PnD, TnH, TnM, TnS, 'duration')

    @classmethod
    def build_interval(cls, start=None, end=None, duration=None):
        return (start, end, duration, 'interval')

    @classmethod
    def build_repeating_interval(cls, R=None, Rnn=None, interval=None):
        return (R, Rnn, interval, 'repeatinginterval')

    @classmethod
    def build_timezone(cls, negative=None, Z=None, hh=None, mm=None, name=''):
        return (negative, Z, hh, mm, name, 'timezone')

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
