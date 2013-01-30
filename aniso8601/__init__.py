# -*- coding: utf-8 -*-

import datetime

def parse_year(yearstr):
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

    if len(yearstr) == 4:
        return datetime.date(int(yearstr), 1, 1)
    else:
        #Shift 0s in from the left to form complete year
        return datetime.date(int(yearstr.ljust(4, '0')), 1, 1)

def parse_calendar_date(datestr):
    #datestr is of the format YYYY-MM-DD, YYYYMMDD, or YYYY-MM
    datestrlen = len(datestr)

    if datestrlen == 10:
        #YYYY-MM-DD
        parseddatetime = datetime.datetime.strptime(datestr, '%Y-%m-%d')

        #Since no 'time' is given, cast to a date
        return parseddatetime.date()
    elif datestrlen == 8:
        #YYYYMMDD
        parseddatetime = datetime.datetime.strptime(datestr, '%Y%m%d')

        #Since no 'time' is given, cast to a date
        return parseddatetime.date()
    elif datestrlen == 7:
        #YYYY-MM
        parseddatetime = datetime.datetime.strptime(datestr, '%Y-%m')

        #Since no 'time' is given, cast to a date
        return parseddatetime.date()
    else:
        raise ValueError('String is not a valid ISO8601 calendar date.')

def parse_week_date(datestr):
    #datestr is of the format YYYY-Www, YYYYWww, YYYY-Www-D, YYYYWwwD
    #
    #W is the week number prefix, ww is the week number, between 1 and 53
    #0 is not a valid week number, which differs from the Python implementation
    #
    #D is the weekday number, between 1 and 7, which differs from the Python
    #implementation which is between 0 and 6

    isoyear = int(datestr[0:4])
    gregorianyearstart = _iso_year_start(isoyear)

    #Week number will be the two characters after the W
    windex = datestr.find('W')
    isoweeknumber = int(datestr[windex + 1:windex + 3])

    if isoweeknumber == 0:
        raise ValueError('00 is not a valid ISO8601 weeknumber.')

    datestrlen = len(datestr)

    if datestr.find('-') != -1:
        if datestrlen == 8:
            #YYYY-Www
            #Suss out the date
            return gregorianyearstart + datetime.timedelta(weeks=isoweeknumber - 1, days=0)
        elif datestrlen == 10:
            #YYYY-Www-D
            isoday = int(datestr[9:10])

            return gregorianyearstart + datetime.timedelta(weeks=isoweeknumber - 1, days=isoday - 1)
        else:
            raise ValueError('String is not a valid ISO8601 week date.')
    else:
        if datestrlen == 7:
            #YYYYWww
            return gregorianyearstart + datetime.timedelta(weeks=isoweeknumber - 1, days=0)
        elif datestrlen == 8:
            #YYYYWwwD
            isoday = int(datestr[7:8])

            return gregorianyearstart + datetime.timedelta(weeks=isoweeknumber - 1, days=isoday - 1)
        else:
            raise ValueError('String is not a valid ISO8601 week date.')

def parse_ordinal_date(datestr):
    #datestr is of the format YYYY-DDD or YYYYDDD
    #DDD can be from 1 - 365, this matches Python's definition

    if datestr.find('-') != -1:
        #YYYY-DDD
        parseddatetime = datetime.datetime.strptime(datestr, '%Y-%j')

        #Since no 'time' is given, cast to a date
        return parseddatetime.date()
    else:
        #YYYYDDD
        parseddatetime = datetime.datetime.strptime(datestr, '%Y%j')

        #Since no 'time' is given, cast to a date
        return parseddatetime.date()

def parse_time(timestr):
    #timestr is of the format hh:mm:ss, hh:mm, hhmmss, hhmm, hh
    #
    #hh is between 0 and 24, 24 is not allowed in the Python time format, since
    #it represents midnight, a time of 00:00:00 is returned
    #
    #mm is between 0 and 60, with 60 used to denote a leap second

    if timestr.count(':') == 2:
        #hh:mm:ss
        timestrarray = timestr.split(':')

        isohour = int(timestrarray[0])
        isominute = int(timestrarray[1])

        if isominute > 60:
            raise ValueError('String is not a valid ISO8601 time.')

        if isohour == 24:
            return datetime.time(hour=0, minute=0)

        #Since the time constructor doesn't handle fractional seconds, we put
        #the seconds in to a timedelta, and add it to the time before returning
        secondsdelta = datetime.timedelta(seconds = float(timestrarray[2]))

        #Now combine todays date (just so we have a date object), the time, the
        #delta, and return the time component
        return (datetime.datetime.combine(datetime.date.today(), datetime.time(hour=isohour, minute=isominute)) + secondsdelta).time()
    elif timestr.count(':') == 1:
        #hh:mm
        timestrarray = timestr.split(':')

        isohour = int(timestrarray[0])
        isominute = float(timestrarray[1]) #Minute may now be a fraction

        if isominute > 60:
            raise ValueError('String is not a valid ISO8601 time.')

        if isohour == 24:
            return datetime.time(hour=0, minute=0)

        #Since the time constructor doesn't handle fractional minutes, we put
        #the minutes in to a timedelta, and add it to the time before returning
        minutesdelta = datetime.timedelta(minutes = isominute)

        #Now combine todays date (just so we have a date object), the time, the
        #delta, and return the time component
        return (datetime.datetime.combine(datetime.date.today(), datetime.time(hour=isohour)) + minutesdelta).time()
    else:
        #Format must be hhmmss, hhmm, or hh
        if timestr.find('.') == -1:
            #No time fractions
            timestrlen = len(timestr)

            if timestrlen == 6:
                #hhmmss
                isohour = int(timestr[0:2])
                isominute = int(timestr[2:4])
                isosecond = int(timestr[4:6])

                if isominute > 60:
                    raise ValueError('String is not a valid ISO8601 time.')

                if isohour == 24:
                    return datetime.time(hour=0, minute=0)

                return datetime.time(hour=isohour, minute=isominute, second=isosecond)
            elif timestrlen == 4:
                #hhmm
                isohour = int(timestr[0:2])
                isominute = int(timestr[2:4])

                if isominute > 60:
                    raise ValueError('String is not a valid ISO8601 time.')

                if isohour == 24:
                    return datetime.time(hour=0, minute=0)

                return datetime.time(hour=isohour, minute=isominute)
            elif timestrlen == 2:
                #hh
                isohour = int(timestr[0:2])

                if isohour == 24:
                    return datetime.time(hour=0)

                return datetime.time(hour=isohour)
            else:
                raise ValueError('String is not a valid ISO8601 time.')
        else:
            #The lowest order element is a fraction
            timestrlen = len(timestr.split('.')[0])

            if timestrlen == 6:
                #hhmmss.
                isohour = int(timestr[0:2])
                isominute = int(timestr[2:4])

                if isominute > 60:
                    raise ValueError('String is not a valid ISO8601 time.')

                if isohour == 24:
                    return datetime.time(hour=0, minute=0)

                #Since the time constructor doesn't handle fractional seconds, we put
                #the seconds in to a timedelta, and add it to the time before returning
                secondsdelta = datetime.timedelta(seconds = float(timestr[4:]))

                #Now combine todays date (just so we have a date object), the time, the
                #delta, and return the time component
                return (datetime.datetime.combine(datetime.date.today(), datetime.time(hour=isohour, minute=isominute)) + secondsdelta).time()
            elif timestrlen == 4:
                #hhmm.
                isohour = int(timestr[0:2])
                isominute = float(timestr[2:])

                if isominute > 60:
                    raise ValueError('String is not a valid ISO8601 time.')

                if isohour == 24:
                    return datetime.time(hour=0, minute=0)

                #Since the time constructor doesn't handle fractional minutes, we put
                #the minutes in to a timedelta, and add it to the time before returning
                minutesdelta = datetime.timedelta(minutes = isominute)

                #Now combine todays date (just so we have a date object), the time, the
                #delta, and return the time component
                return (datetime.datetime.combine(datetime.date.today(), datetime.time(hour=isohour)) + minutesdelta).time()
            elif timestrlen == 2:
                #hh.
                isohour = float(timestr)

                if isohour == 24:
                    return datetime.time(hour=0, minute=0)

                #Since the time constructor doesn't handle fractional hours, we put
                #the hours in to a timedelta, and add it to the time before returning
                hoursdelta = datetime.timedelta(hours = isohour)

                #Now combine todays date (just so we have a date object), the time, the
                #delta, and return the time component
                return (datetime.datetime.combine(datetime.date.today(), datetime.time(hour=0)) + hoursdelta).time()

def parse_timezone(tzstr):
    #tzstr can be ±hh:mm, ±hhmm, ±hh, the Z case is handled elsewhere

    tzstrlen = len(tzstr)

    if tzstrlen == 6:
        #±hh:mm
        tzhour = int(tzstr[1:3])
        tzminute = int(tzstr[4:6])

        if tzstr[0] == '+':
            return UTCOffset(tzstr, datetime.timedelta(hours=tzhour, minutes=tzminute))
        else:
            if tzhour == 0 and tzminute == 0:
                raise ValueError('String is not a valid ISO8601 time offset.')
            else:
                return UTCOffset(tzstr, -datetime.timedelta(hours=tzhour, minutes=tzminute))
    elif tzstrlen == 5:
        #±hhmm
        tzhour = int(tzstr[1:3])
        tzminute = int(tzstr[3:5])

        if tzstr[0] == '+':
            return UTCOffset(tzstr, datetime.timedelta(hours=tzhour, minutes=tzminute))
        else:
            if tzhour == 0 and tzminute == 0:
                raise ValueError('String is not a valid ISO8601 time offset.')
            else:
                return UTCOffset(tzstr, -datetime.timedelta(hours=tzhour, minutes=tzminute))
    elif tzstrlen == 3:
        #±hh
        tzhour = int(tzstr[1:3])

        if tzstr[0] == '+':
            return UTCOffset(tzstr, datetime.timedelta(hours=tzhour))
        else:
            if tzhour == 0:
                raise ValueError('String is not a valid ISO8601 time offset.')
            else:
                return UTCOffset(tzstr, -datetime.timedelta(hours=tzhour))
    else:
        raise ValueError('String is not a valid ISO8601 time offset.')

def _iso_year_start(isoyear):
    #Given an ISO year, returns the equivalent of the start of the year on the
    #Gregorian calendar (which is used by Python)
    #Stolen from:
    #http://stackoverflow.com/questions/304256/whats-the-best-way-to-find-the-inverse-of-datetime-isocalendar

    #Determine the location of the 4th of January, the first week of the ISO
    #year in the week containing the 4th of January
    #http://en.wikipedia.org/wiki/ISO_week_date
    fourth_jan = datetime.date(isoyear, 1, 4)

    #Note the conversion from ISO day (1 - 7) and Python day (0 - 6)
    delta = datetime.timedelta(fourth_jan.isoweekday() - 1)

    #Return the start of the year
    return fourth_jan - delta

class UTCOffset(datetime.tzinfo):
    def __init__(self, name, utcdelta):
        self._name = name
        self._utcdelta = utcdelta

    def utcoffset(self, dt):
        return self._utcdelta

    def tzname(self, dt):
        return self._name

    def dst(self, dt):
        #ISO8601 specifies offsets should be different if DST is required,
        #instead of allowing for a DST to be specified
        return None
