# -*- coding: utf-8 -*-

# Copyright (c) 2018, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

from decimal import Decimal, InvalidOperation
from aniso8601.builder import PythonTimeBuilder
from aniso8601.date import parse_date
from aniso8601.exceptions import HoursOutOfBoundsError, ISOFormatError, \
        LeapSecondError, MidnightBoundsError, MinutesOutOfBoundsError, \
        SecondsOutOfBoundsError
from aniso8601.resolution import TimeResolution
from aniso8601.timezone import parse_timezone

def get_time_resolution(isotimestr):
    #Valid time formats are:
    #
    #hh:mm:ss
    #hhmmss
    #hh:mm
    #hhmm
    #hh
    #hh:mm:ssZ
    #hhmmssZ
    #hh:mmZ
    #hhmmZ
    #hhZ
    #hh:mm:ss±hh:mm
    #hhmmss±hh:mm
    #hh:mm±hh:mm
    #hhmm±hh:mm
    #hh±hh:mm
    #hh:mm:ss±hhmm
    #hhmmss±hhmm
    #hh:mm±hhmm
    #hhmm±hhmm
    #hh±hhmm
    #hh:mm:ss±hh
    #hhmmss±hh
    #hh:mm±hh
    #hhmm±hh
    #hh±hh

    timestr = _split_tz(isotimestr)[0]

    if timestr.count(':') == 2:
        #hh:mm:ss
        return TimeResolution.Seconds
    elif timestr.count(':') == 1:
        #hh:mm
        return TimeResolution.Minutes

    #Format must be hhmmss, hhmm, or hh
    if timestr.find('.') == -1:
        #No time fractions
        timestrlen = len(timestr)
    else:
        #The lowest order element is a fraction
        timestrlen = len(timestr.split('.')[0])

    if timestrlen == 6:
        #hhmmss
        return TimeResolution.Seconds
    elif timestrlen == 4:
        #hhmm
        return TimeResolution.Minutes
    elif timestrlen == 2:
        #hh
        return TimeResolution.Hours

    raise ISOFormatError('"{0}" is not a valid ISO 8601 time.'.format(isotimestr))

def parse_time(isotimestr):
    #Given a string in any ISO 8601 time format, return a datetime.time object
    #that corresponds to the given time. Fixed offset tzdata will be included
    #if UTC offset is given in the input string. Valid time formats are:
    #
    #hh:mm:ss
    #hhmmss
    #hh:mm
    #hhmm
    #hh
    #hh:mm:ssZ
    #hhmmssZ
    #hh:mmZ
    #hhmmZ
    #hhZ
    #hh:mm:ss±hh:mm
    #hhmmss±hh:mm
    #hh:mm±hh:mm
    #hhmm±hh:mm
    #hh±hh:mm
    #hh:mm:ss±hhmm
    #hhmmss±hhmm
    #hh:mm±hhmm
    #hhmm±hhmm
    #hh±hhmm
    #hh:mm:ss±hh
    #hhmmss±hh
    #hh:mm±hh
    #hhmm±hh
    #hh±hh

    (timestr, tzstr) = _split_tz(isotimestr)

    if tzstr is None:
        tzinfo = None
    else:
        tzinfo = parse_timezone(tzstr)

    return _RESOLUTION_MAP[get_time_resolution(timestr)](timestr, tzinfo)

def parse_datetime(isodatetimestr, delimiter='T'):
    #Given a string in ISO 8601 date time format, return a datetime.datetime
    #object that corresponds to the given date time.
    #By default, the ISO 8601 specified T delimiter is used to split the
    #date and time (<date>T<time>). Fixed offset tzdata will be included
    #if UTC offset is given in the input string.

    isodatestr, isotimestr = isodatetimestr.split(delimiter)

    datepart = parse_date(isodatestr)

    timepart = parse_time(isotimestr)

    return PythonTimeBuilder.combine(datepart, timepart)

def _parse_hour(timestr, tzinfo):
    #Format must be hh or hh.
    try:
        isohour = Decimal(timestr)
    except InvalidOperation:
        raise ISOFormatError('Invalid hour string.')

    if isohour == 24:
        return PythonTimeBuilder.build_time(hours=0, minutes=0, tzinfo=tzinfo)
    elif isohour > 24:
        raise HoursOutOfBoundsError('Hour must be between 0..24 with 24 representing midnight.')

    return PythonTimeBuilder.build_time(hours=isohour, tzinfo=tzinfo)

def _parse_minute_time(timestr, tzinfo):
    #Format must be hhmm, hhmm., hh:mm or hh:mm.
    if timestr.count(':') == 1:
        #hh:mm or hh:mm.
        timestrarray = timestr.split(':')

        isohour = int(timestrarray[0])

        try:
            isominute = Decimal(timestrarray[1])  #Minute may now be a fraction
        except InvalidOperation:
            raise ISOFormatError('Invalid minute string.')
    else:
        #hhmm or hhmm.
        isohour = int(timestr[0:2])

        try:
            isominute = Decimal(timestr[2:])
        except InvalidOperation:
            raise ISOFormatError('Invalid minute string.')

    if isominute >= 60:
        raise MinutesOutOfBoundsError('Minutes must be less than 60.')

    if isohour == 24:
        if isominute != 0:
            raise MidnightBoundsError('Hour 24 may only represent midnight.')

        return PythonTimeBuilder.build_time(hours=0, minutes=0, tzinfo=tzinfo)

    return PythonTimeBuilder.build_time(hours=isohour, minutes=isominute, tzinfo=tzinfo)

def _parse_second_time(timestr, tzinfo):
    #Format must be hhmmss, hhmmss., hh:mm:ss or hh:mm:ss.
    if timestr.count(':') == 2:
        #hh:mm:ss or hh:mm:ss.
        timestrarray = timestr.split(':')

        isohour = int(timestrarray[0])
        isominute = int(timestrarray[1])

        try:
            isoseconds = Decimal(timestrarray[2])
        except InvalidOperation:
            raise ISOFormatError('Invalid second string.')
    else:
        #hhmmss or hhmmss.
        isohour = int(timestr[0:2])
        isominute = int(timestr[2:4])

        try:
            isoseconds = Decimal(timestr[4:])
        except InvalidOperation:
            raise ISOFormatError('Invalid second string.')

    if isohour == 23 and isominute == 59 and isoseconds == 60:
        #https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is
        raise LeapSecondError('Leap seconds are not supported.')

    if isoseconds >= 60:
        #https://bitbucket.org/nielsenb/aniso8601/issues/13/parsing-of-leap-second-gives-wildly
        raise SecondsOutOfBoundsError('Seconds must be less than 60.')

    if isominute >= 60:
        raise MinutesOutOfBoundsError('Minutes must be less than 60.')

    if isohour == 24:
        #Midnight, see 4.2.1, 4.2.3
        if isominute != 0 or isoseconds != 0:
            raise MidnightBoundsError('Hour 24 may only represent midnight.')

        return PythonTimeBuilder.build_time(hours=0, minutes=0, tzinfo=tzinfo)

    return PythonTimeBuilder.build_time(hours=isohour, minutes=isominute, seconds=isoseconds, tzinfo=tzinfo)

def _split_tz(isotimestr):
    if isotimestr.find('+') != -1:
        timestr = isotimestr[0:isotimestr.find('+')]
        tzstr = isotimestr[isotimestr.find('+'):]
    elif isotimestr.find('-') != -1:
        timestr = isotimestr[0:isotimestr.find('-')]
        tzstr = isotimestr[isotimestr.find('-'):]
    elif isotimestr.endswith('Z'):
        timestr = isotimestr[:-1]
        tzstr = 'Z'
    else:
        timestr = isotimestr
        tzstr = None

    return (timestr, tzstr)

_RESOLUTION_MAP = {
    TimeResolution.Hours: _parse_hour,
    TimeResolution.Minutes: _parse_minute_time,
    TimeResolution.Seconds: _parse_second_time
}
