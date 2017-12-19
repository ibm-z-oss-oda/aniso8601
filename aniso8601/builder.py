# -*- coding: utf-8 -*-

# Copyright (c) 2016, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime

class BaseTimeBuilder(object):
    @staticmethod
    def build_date(year, month, day):
        raise NotImplementedError

    @staticmethod
    def build_time(hours=0, minutes=0, seconds=0, microseconds=0, tzinfo=None):
        raise NotImplementedError

    @staticmethod
    def build_datetime(year, month, day, hours=0, minutes=0, seconds=0, microseconds=0, tzinfo=None):
        raise NotImplementedError

    @staticmethod
    def build_timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        raise NotImplementedError

    @staticmethod
    def combine(date, time):
        raise NotImplementedError

class PythonTimeBuilder(BaseTimeBuilder):
    @staticmethod
    def build_date(year, month, day):
        return datetime.date(year, month, day)

    @staticmethod
    def build_time(hours=0, minutes=0, seconds=0, microseconds=0, tzinfo=None):
        #Builds a time from the given parts, handling fractional arguments where necessary
        fractional_hours = 0
        fractional_minutes = 0
        fractional_seconds = 0
        fractional_microseconds = 0

        if int(hours) != hours:
            fractional_hours = hours
            hours = 0
        else:
            hours = int(hours)

        if int(minutes) != minutes:
            fractional_minutes = minutes
            minutes = 0
        else:
            minutes = int(minutes)

        if int(seconds) != seconds:
            fractional_seconds = seconds
            seconds = 0
        else:
            seconds = int(seconds)

        if int(microseconds) != microseconds:
            fractional_microseconds = microseconds
            microseconds = 0
        else:
            microseconds = int(microseconds)

        #Datetimes don't handle fractional components, so we use a timedelta
        result_datetime = datetime.datetime(1, 1, 1, hour=hours, minute=minutes, second=seconds, microsecond=microseconds, tzinfo=tzinfo) + PythonTimeBuilder.build_timedelta(seconds=fractional_seconds, microseconds=fractional_microseconds, minutes=fractional_minutes, hours=fractional_hours)

        if tzinfo is None:
            return result_datetime.time()
        else:
            return result_datetime.timetz()

    @staticmethod
    def build_datetime(year, month, day, hours=0, minutes=0, seconds=0, microseconds=0, tzinfo=None):
        #Builds a datetime from the given parts, handling fractional arguments where necessary
        date = datetime.date(year, month, day)
        time = PythonTimeBuilder.build_time(hours=0, minutes=0, seconds=0, microseconds=0, tzinfo=tzinfo)

        return PythonTimeBuilder.combine(date, time)

    @staticmethod
    def build_timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return datetime.timedelta(days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)

    @staticmethod
    def combine(date, time):
        return datetime.datetime.combine(date, time)

class RelativeTimeBuilder(PythonTimeBuilder):
    @staticmethod
    def build_timedelta(years=0, months=0, weeks=0, days=0, hours=0, minutes=0, seconds=0, microseconds=0):
        try:
            import dateutil.relativedelta

            if int(years) != years or int(months) != months:
                #https://github.com/dateutil/dateutil/issues/40
                raise ValueError('Fractional months and years are not defined for relative intervals.')

            return dateutil.relativedelta.relativedelta(years=int(years), months=int(months), weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds, microseconds=microseconds)
        except ImportError:
            raise RuntimeError('dateutil must be installed for relativedelta support.')
