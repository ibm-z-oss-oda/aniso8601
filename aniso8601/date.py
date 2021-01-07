# -*- coding: utf-8 -*-

# Copyright (c) 2021, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

from aniso8601.exceptions import ISOFormatError
from aniso8601.builders import TupleBuilder
from aniso8601.builders.python import PythonTimeBuilder
from aniso8601.compat import is_string
from aniso8601.exceptions import ISOFormatError
from aniso8601.resolution import DateResolution

def get_date_resolution(isodatestr):
    #Valid string formats are:
    #
    #Y[YYY]
    #YYYY-MM-DD
    #YYYYMMDD
    #YYYY-MM
    #YYYY-Www
    #YYYYWww
    #YYYY-Www-D
    #YYYYWwwD
    #YYYY-DDD
    #YYYYDDD
    isodatetuple = parse_date(isodatestr, builder=TupleBuilder)

    if isodatetuple[5] is not None:
        #YYYY-DDD
        #YYYYDDD
        return DateResolution.Ordinal

    if isodatetuple[4] is not None:
        #YYYY-Www-D
        #YYYYWwwD
        return DateResolution.Weekday

    if isodatetuple[3] is not None:
        #YYYY-Www
        #YYYYWww
        return DateResolution.Week

    if isodatetuple[2] is not None:
        #YYYY-MM-DD
        #YYYYMMDD
        return DateResolution.Day

    if isodatetuple[1] is not None:
        #YYYY-MM
        return DateResolution.Month

    #Y[YYY]
    return DateResolution.Year

def parse_date(isodatestr, builder=PythonTimeBuilder):
    #Given a string in any ISO 8601 date format, return a datetime.date
    #object that corresponds to the given date. Valid string formats are:
    #
    #Y[YYY]
    #YYYY-MM-DD
    #YYYYMMDD
    #YYYY-MM
    #YYYY-Www
    #YYYYWww
    #YYYY-Www-D
    #YYYYWwwD
    #YYYY-DDD
    #YYYYDDD
    if is_string(isodatestr) is False:
        raise ValueError('Date must be string.')

    if isodatestr.startswith('+') or isodatestr.startswith('-'):
        raise NotImplementedError('ISO 8601 extended year representation '
                                  'not supported.')

    if len(isodatestr) == 0 or isodatestr.count('-') > 2:
        raise ISOFormatError('"{0}" is not a valid ISO 8601 date.'
                             .format(isodatestr))

    yearstr = None
    monthstr = None
    daystr = None
    weekstr = None
    weekdaystr = None
    ordinaldaystr = None

    #Consume the date components
    componentstr = ''

    for charidx, datechar in enumerate(isodatestr):
        if datechar.isdigit() or (componentstr == '' and yearstr is not None and datechar == 'W'):
            componentstr += datechar
        elif datechar == '-':
            pass
        else:
            raise ISOFormatError('"{0}" is not a valid ISO 8601 date.'
                                 .format(isodatestr))

        if yearstr is None:
            #Y[YYY]
            if len(componentstr) == 4 or charidx == len(isodatestr) - 1:
                yearstr = componentstr
                componentstr = ''
            elif datechar == '-':
                raise ISOFormatError('"{0}" is not a valid ISO 8601 date.'
                                     .format(isodatestr))
        elif yearstr is not None and componentstr != '' and componentstr[0] == 'W':
            #YYYY-Www
            #YYYY-Www-D
            #YYYYWwwD
            if len(componentstr) == 3 and componentstr[0] == 'W':
                weekstr = componentstr[1:]
                componentstr = ''
        elif yearstr is not None and monthstr is None and weekstr is None:
            if len(componentstr) == 2 and (len(isodatestr[charidx + 1:]) >= 2 or (isodatestr[charidx - 2] == '-' and charidx == len(isodatestr) - 1)):
                #YYYY-MM-DD
                #YYYY-MM
                monthstr = componentstr
                componentstr = ''
            elif len(componentstr) == 3 and charidx == len(isodatestr) - 1:
                #YYYY-DDD
                ordinaldaystr = componentstr
                componentstr = ''
        elif yearstr is not None and monthstr is not None:
            #YYYY-MM-DD
            #YYYYMMDD
            if len(componentstr) == 2:
                daystr = componentstr
                componentstr = ''
        elif yearstr is not None and weekstr is not None and weekdaystr is None:
            #YYYY-Www-D
            if len(componentstr) == 1:
                weekdaystr = componentstr
                componentstr = ''
        else:
            raise ISOFormatError('"{0}" is not a valid ISO 8601 date.'
                                 .format(isodatestr))

    if componentstr != '':
        raise ISOFormatError('"{0}" is not a valid ISO 8601 date.'
                             .format(isodatestr))

    return builder.build_date(YYYY=yearstr, MM=monthstr, DD=daystr, Www=weekstr, D=weekdaystr, DDD=ordinaldaystr)
