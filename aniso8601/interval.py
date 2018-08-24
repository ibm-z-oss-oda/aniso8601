# -*- coding: utf-8 -*-

# Copyright (c) 2018, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

from aniso8601.builder import NoneBuilder, PythonTimeBuilder, RelativeTimeBuilder
from aniso8601.date import parse_date
from aniso8601.duration import parse_duration
from aniso8601.exceptions import ISOFormatError
from aniso8601.time import parse_datetime

def parse_interval(isointervalstr, intervaldelimiter='/', datetimedelimiter='T', relative=False, builder=PythonTimeBuilder):
    #Given a string representing an ISO 8601 interval, return a
    #tuple of datetime.date or date.datetime objects representing the beginning
    #and end of the specified interval. Valid formats are:
    #
    #<start>/<end>
    #<start>/<duration>
    #<duration>/<end>
    #
    #The <start> and <end> values can represent dates, or datetimes,
    #not times.
    #
    #The format:
    #
    #<duration>
    #
    #Is expressly not supported as there is no way to provide the addtional
    #required context.

    if isointervalstr[0] == 'R':
        raise ISOFormatError('ISO 8601 repeating intervals must be parsed with parse_repeating_interval.')

    if relative is True:
        builder = RelativeTimeBuilder

    return _parse_interval(isointervalstr, builder, intervaldelimiter, datetimedelimiter)

def parse_repeating_interval(isointervalstr, intervaldelimiter='/', datetimedelimiter='T', relative=False, builder=PythonTimeBuilder):
    #Given a string representing an ISO 8601 interval repating, return a
    #generator of datetime.date or date.datetime objects representing the
    #dates specified by the repeating interval. Valid formats are:
    #
    #Rnn/<interval>
    #R/<interval>

    if isointervalstr[0] != 'R':
        raise ISOFormatError('ISO 8601 repeating interval must start with an R.')

    if relative is True:
        builder = RelativeTimeBuilder

    #Parse the number of iterations
    iterationpart, intervalpart = isointervalstr.split(intervaldelimiter, 1)

    if len(iterationpart) > 1:
        R = False
        Rnn = iterationpart[1:]
    else:
        R = True
        Rnn = None

    interval = _parse_interval(intervalpart, NoneBuilder, intervaldelimiter, datetimedelimiter)

    return builder.build_repeating_interval(R=R, Rnn=Rnn, interval=interval)

def _parse_interval(isointervalstr, builder, intervaldelimiter='/', datetimedelimiter='T'):
    #Returns a tuple containing the start of the interval and the end of the interval

    firstpart, secondpart = isointervalstr.split(intervaldelimiter)

    if firstpart[0] == 'P':
        #<duration>/<end>
        #Notice that these are not returned 'in order' (earlier to later), this
        #is to maintain consistency with parsing <start>/<end> durations, as
        #well as making repeating interval code cleaner. Users who desire
        #durations to be in order can use the 'sorted' operator.

        #We need to figure out if <end> is a date, or a datetime
        if secondpart.find(datetimedelimiter) != -1:
            #<end> is a datetime
            duration = parse_duration(firstpart, builder=NoneBuilder)
            enddatetime = parse_datetime(secondpart, delimiter=datetimedelimiter, builder=NoneBuilder)

            return builder.build_interval(end=enddatetime, duration=duration)

        #<end> must just be a date
        duration = parse_duration(firstpart, builder=NoneBuilder)
        enddate = parse_date(secondpart, builder=NoneBuilder)

        return builder.build_interval(end=enddate, duration=duration)
    elif secondpart[0] == 'P':
        #<start>/<duration>
        #We need to figure out if <start> is a date, or a datetime
        if firstpart.find(datetimedelimiter) != -1:
            #<start> is a datetime
            duration = parse_duration(secondpart, builder=NoneBuilder)
            startdatetime = parse_datetime(firstpart, delimiter=datetimedelimiter, builder=NoneBuilder)

            return builder.build_interval(start=startdatetime, duration=duration)

        #<start> must just be a date
        duration = parse_duration(secondpart, builder=NoneBuilder)
        startdate = parse_date(firstpart, builder=NoneBuilder)

        return builder.build_interval(start=startdate, duration=duration)

    #<start>/<end>
    if firstpart.find(datetimedelimiter) != -1 and secondpart.find(datetimedelimiter) != -1:
        #Both parts are datetimes
        start_datetime = parse_datetime(firstpart, delimiter=datetimedelimiter, builder=NoneBuilder)
        end_datetime = parse_datetime(secondpart, delimiter=datetimedelimiter, builder=NoneBuilder)

        return builder.build_interval(start=start_datetime, end=end_datetime)
    elif firstpart.find(datetimedelimiter) != -1 and secondpart.find(datetimedelimiter) == -1:
        #First part is a datetime, second part is a date
        start_datetime = parse_datetime(firstpart, delimiter=datetimedelimiter, builder=NoneBuilder)
        end_date = parse_date(secondpart, builder=NoneBuilder)

        return builder.build_interval(start=start_datetime, end=end_date)
    elif firstpart.find(datetimedelimiter) == -1 and secondpart.find(datetimedelimiter) != -1:
        #First part is a date, second part is a datetime
        start_date = parse_date(firstpart, builder=NoneBuilder)
        end_datetime = parse_datetime(secondpart, delimiter=datetimedelimiter, builder=NoneBuilder)

        return builder.build_interval(start=start_date, end=end_datetime)

    #Both parts are dates
    start_date = parse_date(firstpart, builder=NoneBuilder)
    end_date = parse_date(secondpart, builder=NoneBuilder)

    return builder.build_interval(start=start_date, end=end_date)
