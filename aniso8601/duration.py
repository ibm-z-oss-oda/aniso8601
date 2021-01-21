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
        parseresult = _parse_duration_prescribed(isodurationstr)
        return builder.build_duration(**parseresult)

    if isodurationstr.find('T') != -1:
        parseresult = _parse_duration_combined(isodurationstr)
        return builder.build_duration(**parseresult)

    raise ISOFormatError('"{0}" is not a valid ISO 8601 duration.'
                          .format(isodurationstr))

def _parse_duration_prescribed(durationstr):
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
        return _parse_duration_prescribed_notime(durationstr)

    return _parse_duration_prescribed_time(durationstr)

def _parse_duration_prescribed_notime(isodurationstr):
    #durationstr can be of the form PnYnMnD or PnW

    durationstr = normalize(isodurationstr)

    yearstr = None
    monthstr = None
    daystr = None
    weekstr = None

    weekidx = durationstr.find('W')
    yearidx = durationstr.find('Y')
    monthidx = durationstr.find('M')
    dayidx = durationstr.find('D')

    if weekidx != -1:
        weekstr = durationstr[1:-1]
    elif yearidx != -1 and monthidx != -1 and dayidx != -1:
        yearstr = durationstr[1:yearidx]
        monthstr = durationstr[yearidx + 1:monthidx]
        daystr = durationstr[monthidx + 1:-1]
    elif yearidx != -1 and monthidx != -1:
        yearstr = durationstr[1:yearidx]
        monthstr = durationstr[yearidx + 1:monthidx]
    elif monthidx != -1 and dayidx != -1:
        monthstr = durationstr[1:monthidx]
        daystr = durationstr[monthidx + 1:-1]
    elif yearidx != -1:
        yearstr = durationstr[1:-1]
    elif monthidx != -1:
        monthstr = durationstr[1:-1]
    elif dayidx != -1:
        daystr = durationstr[1:-1]
    else:
        raise ISOFormatError('"{0}" is not a valid ISO 8601 duration.'
                              .format(isodurationstr))

    hascomponent = False

    for componentstr in [yearstr, monthstr, daystr, weekstr]:
        if componentstr is not None:
            hascomponent = True

            if '.' in componentstr:
                intstr, fractionalstr = componentstr.split('.', 1)

                if intstr.isdigit() is False:
                    raise ISOFormatError('"{0}" is not a valid ISO 8601 duration.'
                                          .format(isodurationstr))

                if fractionalstr.isdigit() is False:
                    raise ISOFormatError('"{0}" is not a valid ISO 8601 duration.'
                                          .format(isodurationstr))
            else:
                if componentstr.isdigit() is False:
                    raise ISOFormatError('"{0}" is not a valid ISO 8601 duration.'
                                          .format(isodurationstr))

    if hascomponent is False:
        raise ISOFormatError('"{0}" is not a valid ISO 8601 duration.'
                              .format(isodurationstr))

    return {'PnY': yearstr, 'PnM': monthstr, 'PnW': weekstr, 'PnD': daystr}

def _parse_duration_prescribed_time(isodurationstr):
    #durationstr can be of the form PnYnMnDTnHnMnS

    timeidx = isodurationstr.find('T')

    datestr = isodurationstr[:timeidx]
    timestr = normalize(isodurationstr[timeidx + 1:])

    hourstr = None
    minutestr = None
    secondstr = None

    houridx = timestr.find('H')
    minuteidx = timestr.find('M')
    secondidx = timestr.find('S')

    if houridx != -1 and minuteidx != -1 and secondidx != -1:
        hourstr = timestr[0:houridx]
        minutestr = timestr[houridx + 1:minuteidx]
        secondstr = timestr[minuteidx + 1:-1]
    elif houridx != -1 and minuteidx != -1:
        hourstr = timestr[0:houridx]
        minutestr = timestr[houridx + 1:minuteidx]
    elif minuteidx != -1 and secondidx != -1:
        minutestr = timestr[0:minuteidx]
        secondstr = timestr[minuteidx + 1:-1]
    elif houridx != -1:
        hourstr = timestr[0:-1]
    elif minuteidx != -1:
        minutestr = timestr[0:-1]
    elif secondidx != -1:
        secondstr = timestr[0:-1]
    else:
        raise ISOFormatError('"{0}" is not a valid ISO 8601 duration.'
                              .format(isodurationstr))

    hascomponent = False

    for componentstr in [hourstr, minutestr, secondstr]:
        if componentstr is not None:
            hascomponent = True

            if '.' in componentstr:
                intstr, fractionalstr = componentstr.split('.', 1)

                if intstr.isdigit() is False:
                    raise ISOFormatError('"{0}" is not a valid ISO 8601 duration.'
                                          .format(isodurationstr))

                if fractionalstr.isdigit() is False:
                    raise ISOFormatError('"{0}" is not a valid ISO 8601 duration.'
                                          .format(isodurationstr))
            else:
                if componentstr.isdigit() is False:
                    raise ISOFormatError('"{0}" is not a valid ISO 8601 duration.'
                                          .format(isodurationstr))

    if hascomponent is False:
        raise ISOFormatError('"{0}" is not a valid ISO 8601 duration.'
                              .format(isodurationstr))

    #Parse any date components
    durationdict = {'PnY': None, 'PnM': None, 'PnW': None, 'PnD': None}

    if len(datestr) > 1:
        durationdict = _parse_duration_prescribed_notime(datestr)

    durationdict.update({'TnH': hourstr, 'TnM': minutestr, 'TnS': secondstr})

    return durationdict

def _parse_duration_combined(durationstr):
    #Period of the form P<date>T<time>

    #Split the string in to its component parts
    datepart, timepart = durationstr[1:].split('T', maxsplit=1) #We skip the 'P'

    datevalue = parse_date(datepart, builder=TupleBuilder)
    timevalue = parse_time(timepart, builder=TupleBuilder)

    return {'PnY': datevalue.YYYY, 'PnM': datevalue.MM, 'PnD': datevalue.DD,
            'TnH': timevalue.hh, 'TnM': timevalue.mm, 'TnS': timevalue.ss}

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
