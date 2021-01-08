# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

from aniso8601.builders import TupleBuilder
from aniso8601.builders.python import PythonTimeBuilder
from aniso8601.compat import is_string
from aniso8601.date import parse_date
from aniso8601.decimalfraction import find_separator, normalize
from aniso8601.exceptions import ISOFormatError
from aniso8601.resolution import TimeResolution
from aniso8601.timezone import parse_timezone

TIMEZONE_DELIMITERS = ['Z', '+', '-']

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
    isotimetuple = parse_time(isotimestr, builder=TupleBuilder)

    if isotimetuple[2] is not None:
        return TimeResolution.Seconds

    if isotimetuple[1] is not None:
        return TimeResolution.Minutes

    return TimeResolution.Hours

def parse_time(isotimestr, builder=PythonTimeBuilder):
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
    if is_string(isotimestr) is False:
        raise ValueError('Time must be string.')

    if len(isotimestr) == 0:
        raise ISOFormatError('"{0}" is not a valid ISO 8601 time.'
                             .format(isotimestr))

    timestr = normalize(isotimestr)

    hourstr = None
    minutestr = None
    secondstr = None
    tzstr = None

    hasfractionalcomponent = False
    parsingtz = False

    #Consume the time components
    componentstr = ''

    for charidx, timechar in enumerate(timestr):
        if timechar.isdigit():
            componentstr += timechar
        elif timechar == '.' and hasfractionalcomponent is False:
            componentstr += timechar
            hasfractionalcomponent = True
        elif parsingtz is True and timechar == ':':
            componentstr += timechar
        elif timechar == ':' or timechar in TIMEZONE_DELIMITERS:
            pass
        else:
            raise ISOFormatError('"{0}" is not a valid ISO 8601 time.'
                                 .format(isotimestr))

        parsecomponent = False

        if parsingtz is False:
            if len(componentstr) == 2 and charidx < len(isotimestr) - 1 and timestr[charidx + 1].isdigit():
                #Lookahead, if we have two characters, and the next is a number, parse
                parsecomponent = True
            elif componentstr != '' and (timechar == ':' or timechar in TIMEZONE_DELIMITERS):
                #If we've consumed characaters, and we hit a colon or TZ, parse
                parsecomponent = True
            elif charidx == len(timestr) - 1:
                #We're at the end of the string, parse
                parsecomponent = True

        if parsecomponent is True and hasfractionalcomponent is True and '.' not in componentstr:
            #Only parse a single fractional component
            raise ISOFormatError('"{0}" is not a valid ISO 8601 time.'
                                 .format(isotimestr))

        if hourstr is None:
            if parsecomponent is True:
                hourstr = componentstr
                componentstr = ''
        elif hourstr is not None and minutestr is None and parsingtz is False:
            if parsecomponent is True:
                minutestr = componentstr
                componentstr = ''
        elif hourstr is not None and minutestr is not None and secondstr is None and parsingtz is False:
            if parsecomponent is True:
                secondstr = componentstr
                componentstr = ''
        elif hourstr is not None and tzstr is None and timechar in TIMEZONE_DELIMITERS:
            #Avoid an error parsing 'Z' before parsingtz is set
            pass
        elif hourstr is not None and tzstr is None and parsingtz is True:
            if charidx == len(timestr) - 1:
                tzstr = componentstr
                componentstr = ''
                parsingtz = False
        else:
            raise ISOFormatError('"{0}" is not a valid ISO 8601 time.'
                                 .format(isotimestr))

        if timechar in TIMEZONE_DELIMITERS and parsingtz is False:
            if timechar == 'Z':
                tzstr = 'Z'
                componentstr = ''
            else:
                parsingtz = True
                componentstr = timechar

    if componentstr != '':
        raise ISOFormatError('"{0}" is not a valid ISO 8601 time.'
                             .format(isotimestr))

    if tzstr is None:
        tz = None
    else:
        tz = parse_timezone(tzstr, builder=TupleBuilder)

    return builder.build_time(hh=hourstr, mm=minutestr, ss=secondstr, tz=tz)

def parse_datetime(isodatetimestr, delimiter='T', builder=PythonTimeBuilder):
    #Given a string in ISO 8601 date time format, return a datetime.datetime
    #object that corresponds to the given date time.
    #By default, the ISO 8601 specified T delimiter is used to split the
    #date and time (<date>T<time>). Fixed offset tzdata will be included
    #if UTC offset is given in the input string.
    if is_string(isodatetimestr) is False:
        raise ValueError('Date time must be string.')

    if delimiter not in isodatetimestr:
        raise ISOFormatError('Delimiter "{0}" is not in combined date time '
                             'string "{1}".'
                             .format(delimiter, isodatetimestr))

    isodatestr, isotimestr = isodatetimestr.split(delimiter, 1)

    datepart = parse_date(isodatestr, builder=TupleBuilder)

    timepart = parse_time(isotimestr, builder=TupleBuilder)

    return builder.build_datetime(datepart, timepart)
