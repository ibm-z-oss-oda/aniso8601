# -*- coding: utf-8 -*-

# Copyright (c) 2018, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

from aniso8601.exceptions import DayOutOfBoundsError, ISOFormatError, \
        WeekOutOfBoundsError
from aniso8601.builder import PythonTimeBuilder
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
    if isodatestr.startswith('+') or isodatestr.startswith('-'):
        raise NotImplementedError('ISO 8601 extended year representation not supported.')

    if isodatestr.find('W') != -1:
        #Handle ISO 8601 week date format
        hyphens_present = 1 if isodatestr.find('-') != -1 else 0
        week_date_len = 7 + hyphens_present
        weekday_date_len = 8 + 2 * hyphens_present

        if len(isodatestr) == week_date_len:
            #YYYY-Www
            #YYYYWww
            return DateResolution.Week
        elif len(isodatestr) == weekday_date_len:
            #YYYY-Www-D
            #YYYYWwwD
            return DateResolution.Weekday
        else:
            raise ISOFormatError('"{0}" is not a valid ISO 8601 week date.'.format(isodatestr))

    #If the size of the string of 4 or less, assume its a truncated year representation
    if len(isodatestr) <= 4:
        return DateResolution.Year

    #An ISO string may be a calendar represntation if:
    # 1) When split on a hyphen, the sizes of the parts are 4, 2, 2 or 4, 2
    # 2) There are no hyphens, and the length is 8
    datestrsplit = isodatestr.split('-')

    #Check case 1
    if len(datestrsplit) == 2:
        if len(datestrsplit[0]) == 4 and len(datestrsplit[1]) == 2:
            return DateResolution.Month

    if len(datestrsplit) == 3:
        if len(datestrsplit[0]) == 4 and len(datestrsplit[1]) == 2 and len(datestrsplit[2]) == 2:
            return DateResolution.Day

    #Check case 2
    if len(isodatestr) == 8 and isodatestr.find('-') == -1:
        return DateResolution.Day

    #An ISO string may be a ordinal date representation if:
    # 1) When split on a hyphen, the sizes of the parts are 4, 3
    # 2) There are no hyphens, and the length is 7

    #Check case 1
    if len(datestrsplit) == 2:
        if len(datestrsplit[0]) == 4 and len(datestrsplit[1]) == 3:
            return DateResolution.Ordinal

    #Check case 2
    if len(isodatestr) == 7 and isodatestr.find('-') == -1:
        return DateResolution.Ordinal

    #None of the date representations match
    raise ISOFormatError('"{0}" is not an ISO 8601 date, perhaps it represents a time or datetime.'.format(isodatestr))

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
    #
    #Note that the ISO 8601 date format of ±YYYYY is expressly not supported
    return _RESOLUTION_MAP[get_date_resolution(isodatestr)](isodatestr, builder)

def _parse_year(yearstr, builder):
    #yearstr is of the format Y[YYY]
    #
    #0000 (1 BC) is not representible as a Python date so a ValueError is
    #raised
    #
    #Truncated dates, like '19', refer to 1900-1999 inclusive, we simply parse
    #to 1900-01-01
    #
    #Since no additional resolution is provided, the month is set to 1, and
    #day is set to 1

    if len(yearstr) < 4:
        #Shift 0s in from the left to form complete year
        yearstr = yearstr.ljust(4, '0')

    return builder.build_date(yearstr, 1, 1)

def _parse_calendar_day(datestr, builder):
    #datestr is of the format YYYY-MM-DD or YYYYMMDD
    if len(datestr) == 10:
        #YYYY-MM-DD
        yearstr = datestr[0:4]
        monthstr = datestr[5:7]
        daystr = datestr[8:]
    elif len(datestr) == 8:
        #YYYYMMDD
        yearstr = datestr[0:4]
        monthstr = datestr[4:6]
        daystr = datestr[6:]
    else:
        raise ISOFormatError('"{0}" is not a valid ISO 8601 calendar day.'.format(datestr))

    return builder.build_date(yearstr, monthstr, daystr)

def _parse_calendar_month(datestr, builder):
    #datestr is of the format YYYY-MM
    if len(datestr) != 7:
        raise ISOFormatError('"{0}" is not a valid ISO 8601 calendar month.'.format(datestr))

    yearstr = datestr[0:4]
    monthstr = datestr[5:]

    return builder.build_date(yearstr, monthstr, 1)

def _parse_week_day(datestr, builder):
    #datestr is of the format YYYY-Www-D, YYYYWwwD
    #
    #W is the week number prefix, ww is the week number, between 1 and 53
    #0 is not a valid week number, which differs from the Python implementation
    #
    #D is the weekday number, between 1 and 7, which differs from the Python
    #implementation which is between 0 and 6

    #TODO: Avoid casting back and forth from int to string
    isoyear = int(datestr[0:4])
    gregorianyearstart = _iso_year_start(isoyear, builder)

    #Week number will be the two characters after the W
    windex = datestr.find('W')
    isoweeknumber = int(datestr[windex + 1:windex + 3])

    if isoweeknumber == 0 or isoweeknumber > 53:
        raise WeekOutOfBoundsError('Week number must be between 1..53.')

    if datestr.find('-') != -1 and len(datestr) == 10:
        #YYYY-Www-D
        isoday = int(datestr[9:10])
    elif len(datestr) == 8:
         #YYYYWwwD
        isoday = int(datestr[7:8])
    else:
        raise ISOFormatError('"{0}" is not a valid ISO 8601 week date.'.format(datestr))

    if isoday == 0 or isoday > 7:
        raise DayOutOfBoundsError('Weekday number must be between 1..7.')

    return gregorianyearstart + builder.build_timedelta(weeks=str(isoweeknumber - 1), days=str(isoday - 1))

def _parse_week(datestr, builder):
    #datestr is of the format YYYY-Www, YYYYWww
    #
    #W is the week number prefix, ww is the week number, between 1 and 53
    #0 is not a valid week number, which differs from the Python implementation

    #TODO: Avoid casting back and forth from int to string
    isoyear = int(datestr[0:4])
    gregorianyearstart = _iso_year_start(isoyear, builder)

    #Week number will be the two characters after the W
    windex = datestr.find('W')
    isoweeknumber = int(datestr[windex + 1:windex + 3])

    if isoweeknumber == 0 or isoweeknumber > 53:
        raise WeekOutOfBoundsError('Week number must be between 1..53.')

    return gregorianyearstart + builder.build_timedelta(weeks=str(isoweeknumber - 1), days=str(0))

def _parse_ordinal_date(datestr, builder):
    #datestr is of the format YYYY-DDD or YYYYDDD
    #DDD can be from 1 - 36[5,6], this matches Python's definition

    #TODO: Avoid casting back and forth from int to string
    isoyear = int(datestr[0:4])

    if datestr.find('-') != -1:
        #YYYY-DDD
        isoday = int(datestr[(datestr.find('-') + 1):])
    else:
        #YYYYDDD
        isoday = int(datestr[4:])

    #Day of year to a date
    #https://stackoverflow.com/questions/2427555/python-question-year-and-day-of-year-to-date
    parseddate = builder.build_date(str(isoyear), str(1), str(1)) + PythonTimeBuilder.build_timedelta(days=str(isoday - 1))

    #Enforce ordinal day limitation
    #https://bitbucket.org/nielsenb/aniso8601/issues/14/parsing-ordinal-dates-should-only-allow
    if isoday == 0 or parseddate.year != isoyear:
        raise DayOutOfBoundsError('Day of year must be from 1..365, 1..366 for leap year.')

    return parseddate

def _iso_year_start(isoyear, builder):
    #Given an ISO year, returns the equivalent of the start of the year
    #on the Gregorian calendar (which is used by Python)
    #Stolen from:
    #http://stackoverflow.com/questions/304256/whats-the-best-way-to-find-the-inverse-of-datetime-isocalendar

    #Determine the location of the 4th of January, the first week of
    #the ISO year is the week containing the 4th of January
    #http://en.wikipedia.org/wiki/ISO_week_date
    fourth_jan = builder.build_date(str(isoyear), str(1), str(4))

    #Note the conversion from ISO day (1 - 7) and Python day (0 - 6)
    delta = builder.build_timedelta(days=str(fourth_jan.isoweekday() - 1))

    #Return the start of the year
    return fourth_jan - delta

_RESOLUTION_MAP = {
    DateResolution.Day: _parse_calendar_day,
    DateResolution.Ordinal: _parse_ordinal_date,
    DateResolution.Month: _parse_calendar_month,
    DateResolution.Week: _parse_week,
    DateResolution.Weekday: _parse_week_day,
    DateResolution.Year: _parse_year
}
