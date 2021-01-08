# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

from aniso8601 import compat
from aniso8601.builders import TupleBuilder
from aniso8601.builders.python import PythonTimeBuilder
from aniso8601.date import parse_date
from aniso8601.decimalfraction import find_separator, normalize
from aniso8601.exceptions import ISOFormatError, NegativeDurationError
from aniso8601.time import parse_time

def parse_duration(isodurationstr, builder=PythonTimeBuilder):
    #Given a string representing an ISO 8601 duration, return a
    #a duration built by the given builder. Valid formats are:
    #
    #PnYnMnDTnHnMnS (or any reduced precision equivalent)
    #P<date>T<time>

    if compat.is_string(isodurationstr) is False:
        raise ValueError('Duration must be string.')

    if len(isodurationstr) == 0:
        raise ISOFormatError('"{0}" is not a valid ISO 8601 duration.'
                .format(isodurationstr))

    if isodurationstr[0] != 'P':
        raise ISOFormatError('ISO 8601 duration must start with a P.')

    #If Y, M, D, H, S, or W are in the string,
    #assume it is a specified duration
    if _has_any_component(isodurationstr,
                          ['Y', 'M', 'D', 'H', 'S', 'W']) is True:
        return _parse_duration_prescribed(isodurationstr, builder)

    if isodurationstr.find('T') != -1:
        return _parse_duration_combined(isodurationstr, builder)

    raise ISOFormatError('"{0}" is not a valid ISO 8601 duration.'
                          .format(isodurationstr))

def _parse_duration_prescribed(durationstr, builder):
    #durationstr can be of the form PnYnMnDTnHnMnS or PnW

    #Don't allow negative elements
    #https://bitbucket.org/nielsenb/aniso8601/issues/20/negative-duration
    if durationstr.find('-') != -1:
        raise NegativeDurationError('ISO 8601 durations must be positive.')

    #Make sure the end character is valid
    #https://bitbucket.org/nielsenb/aniso8601/issues/9/durations-with-trailing-garbage-are-parsed
    if durationstr[-1] not in ['Y', 'M', 'D', 'H', 'S', 'W']:
        raise ISOFormatError('ISO 8601 duration must end with a valid '
                             'character.')

    #Make sure only the lowest order element has decimal precision
    separator_index = find_separator(durationstr)
    if separator_index != -1:
        remaining = durationstr[separator_index + 1:]
        if find_separator(remaining) != -1:
            raise ISOFormatError('ISO 8601 allows only lowest order element to '
                             'have a decimal fraction.')

        #There should only ever be 1 letter after a decimal if there is more
        #then one, the string is invalid
        lettercount = 0

        for character in remaining:
            if character.isalpha() is True:
                lettercount += 1

                if lettercount > 1:
                    raise ISOFormatError('ISO 8601 duration must end with '
                                         'a single valid character.')

    #Do not allow W in combination with other designators
    #https://bitbucket.org/nielsenb/aniso8601/issues/2/week-designators-should-not-be-combinable
    if (durationstr.find('W') != -1
            and _has_any_component(durationstr,
                                   ['Y', 'M', 'D', 'H', 'S']) is True):
        raise ISOFormatError('ISO 8601 week designators may not be combined '
                             'with other time designators.')

    #Parse the elements of the duration
    if durationstr.find('T') == -1:
        return _parse_duration_prescribed_notime(durationstr, builder)

    return _parse_duration_prescribed_time(durationstr, builder)

def _parse_duration_prescribed_notime(durationstr, builder):
    #durationstr can be of the form PnYnMnD or PnW

    #Don't allow negative elements
    #https://bitbucket.org/nielsenb/aniso8601/issues/20/negative-duration
    if durationstr.find('-') != -1:
        raise NegativeDurationError('ISO 8601 durations must be positive.')

    yearstr = None
    monthstr = None
    weekstr = None
    daystr = None

    #Consume the date components
    componentstr = ''

    for datachar in normalize(durationstr[1:]):
        if datachar.isdigit() or datachar == '.':
            componentstr += datachar
        elif datachar == 'Y' and yearstr is None and monthstr is None and weekstr is None and daystr is None:
            yearstr = componentstr
            componentstr = ''
        elif datachar == 'M' and monthstr is None and weekstr is None and daystr is None:
            monthstr = componentstr
            componentstr = ''
        elif datachar == 'W' and weekstr is None and daystr is None:
            weekstr = componentstr
            componentstr = ''
        elif datachar == 'D' and daystr is None:
            daystr = componentstr
            componentstr = ''
        else:
            raise ISOFormatError('"{0}" is not a valid ISO 8601 duration.'
                                  .format(durationstr))

    #Make sure everything was consumed
    if componentstr != '':
        raise ISOFormatError('"{0}" is not a valid ISO 8601 duration.'
                              .format(durationstr))

    return builder.build_duration(PnY=yearstr, PnM=monthstr,
                                  PnW=weekstr, PnD=daystr)

def _parse_duration_prescribed_time(durationstr, builder):
    #durationstr can be of the form PnYnMnDTnHnMnS

    #Don't allow negative elements
    #https://bitbucket.org/nielsenb/aniso8601/issues/20/negative-duration
    if durationstr.find('-') != -1:
        raise NegativeDurationError('ISO 8601 durations must be positive.')

    timeidx = durationstr.find('T')

    firsthalf = durationstr[1:timeidx]
    secondhalf = normalize(durationstr[timeidx + 1:])

    yearstr = None
    monthstr = None
    daystr = None
    hourstr = None
    minutestr = None
    secondstr = None

    #Consume the date components
    componentstr = ''

    for datachar in firsthalf:
        if datachar.isdigit():
            componentstr += datachar
        elif datachar == 'Y' and yearstr is None and monthstr is None and daystr is None:
            yearstr = componentstr
            componentstr = ''
        elif datachar == 'M' and monthstr is None and daystr is None:
            monthstr = componentstr
            componentstr = ''
        elif datachar == 'D' and daystr is None:
            daystr = componentstr
            componentstr = ''
        else:
            raise ISOFormatError('"{0}" is not a valid ISO 8601 duration.'
                                  .format(durationstr))

    #Make sure everything was consumed
    if componentstr != '':
        raise ISOFormatError('"{0}" is not a valid ISO 8601 duration.'
                              .format(durationstr))


    #Consume the time components
    componentstr = ''

    for datachar in secondhalf:
        if datachar.isdigit() or datachar == '.':
            componentstr += datachar
        elif datachar == 'H' and hourstr is None and minutestr is None and secondstr is None:
            hourstr = componentstr
            componentstr = ''
        elif datachar == 'M' and minutestr is None and secondstr is None:
            minutestr = componentstr
            componentstr = ''
        elif datachar == 'S' and secondstr is None:
            secondstr = componentstr
            componentstr = ''
        else:
            raise ISOFormatError('"{0}" is not a valid ISO 8601 duration.'
                                  .format(durationstr))

    #Make sure everything was consumed
    if componentstr != '':
        raise ISOFormatError('"{0}" is not a valid ISO 8601 duration.'
                              .format(durationstr))

    return builder.build_duration(PnY=yearstr, PnM=monthstr, PnD=daystr,
                                  TnH=hourstr, TnM=minutestr, TnS=secondstr)

def _parse_duration_combined(durationstr, builder):
    #Period of the form P<date>T<time>

    #Split the string in to its component parts
    datepart, timepart = durationstr[1:].split('T', maxsplit=1) #We skip the 'P'

    datevalue = parse_date(datepart, builder=TupleBuilder)
    timevalue = parse_time(timepart, builder=TupleBuilder)

    return builder.build_duration(PnY=datevalue[0], PnM=datevalue[1],
                                  PnD=datevalue[2], TnH=timevalue[0],
                                  TnM=timevalue[1], TnS=timevalue[2])

def _has_any_component(durationstr, components):
    #Given a duration string, and a list of components, returns True
    #if any of the listed components are present, False otherwise.
    #
    #For instance:
    #durationstr = 'P1Y'
    #components = ['Y', 'M']
    #
    #returns True
    #
    #durationstr = 'P1Y'
    #components = ['M', 'D']
    #
    #returns False

    for component in components:
        if durationstr.find(component) != -1:
            return True

    return False
