.. _builder_development:

aniso8601 - Builder Development
===============================

Most builders will descend from either :code:`builders.BaseTimeBuilder` or :code:`builders.python.PythonTimeBuilder`.

Builder class variables
=======================

:code:`LEAP_SECONDS_SUPPORTED` (:code:`boolean`, default :code:`False`) - Set to :code:`True` if :code:`range_check_time` should accept `leap seconds <https://en.wikipedia.org/wiki/Leap_second>`_. Otherwise :code:`range_check_time` will raise a :code:`LeapSecondError` when range checking a time representing a leap second.

Limit tuples
------------

The :code:`builders.range_check` method used by the default range check methods operates on limits defined by Limit named tuples

Limit
^^^^^

:code:`casterrorstring` (:code:`str`) - Error message for when cast operation fails
:code:`min` (:code:`int`, :code:`float`, :code:`None`) - Minimum value, value < min raises :code:`rangeexception` with the give :code:`rangerrorstring`, :code:`None` means bound is not enforced
:code:`max` (:code:`int`, :code:`float`, :code:`None`) - Minimum value, value > min raises :code:`rangeexception` with the give :code:`rangerrorstring`, :code:`None` means bound is not enforced
:code:`rangeexception` (:code:`Exception`) - Exception to raise when value is out of given range
:code:`rangeerrorstring` (:code:`str`) - String passed to :code:`rangeexception` constructor when value is out of given range
:code:`rangefunc` (:code:`method`) - Method to call for range checking, must take value as the first argument, and the applicable limit tuple as the second

Limits
------

The limit tuples defined in :code:`BaseTimeBuilder` are defined as follows:

:code:`DATE_YYYY_LIMIT`::

  Limit('Invalid year string.',
        0000, 9999, YearOutOfBoundsError,
        'Year must be between 1..9999.',
        range_check)

:code:`DATE_MM_LIMIT`::

  Limit('Invalid month string.',
        1, 12, MonthOutOfBoundsError,
        'Month must be between 1..12.',
        range_check)

:code:`DATE_DD_LIMIT`::

  Limit('Invalid day string.',
        1, 31, DayOutOfBoundsError,
        'Day must be between 1..31.',
        range_check)

:code:`DATE_WWW_LIMIT`::

  Limit('Invalid week string.',
        1, 53, WeekOutOfBoundsError,
        'Week number must be between 1..53.',
        range_check)

:code:`DATE_D_LIMIT`::

  Limit('Invalid weekday string.',
        1, 7, DayOutOfBoundsError,
        'Weekday number must be between 1..7.',
        range_check)

:code:`DATE_DDD_LIMIT`::

  Limit('Invalid ordinal day string.',
        1, 366, DayOutOfBoundsError,
        'Ordinal day must be between 1..366.',
        range_check)

:code:`TIME_HH_LIMIT`::

  Limit('Invalid hour string.',
        0, 24, HoursOutOfBoundsError,
        'Hour must be between 0..24 with '
        '24 representing midnight.',
        range_check)

:code:`TIME_MM_LIMIT`::

  Limit('Invalid minute string.',
        0, 59, MinutesOutOfBoundsError,
        'Minute must be between 0..59.',
        range_check)

:code:`TIME_SS_LIMIT`::

  Limit('Invalid second string.',
        0, 60, SecondsOutOfBoundsError,
        'Second must be between 0..60 with 60 representing a leap second.',
        range_check)

:code:`TZ_HH_LIMIT`::

  Limit('Invalid timezone hour string.',
        0, 23, HoursOutOfBoundsError,
        'Hour must be between 0..23.',
        range_check)

:code:`TZ_MM_LIMIT`::

  Limit('Invalid timezone minute string.',
        0, 59, MinutesOutOfBoundsError,
        'Minute must be between 0..59.',
        range_check)

:code:`DURATION_PNY_LIMIT`::

  Limit('Invalid year duration string.',
        0, None, ISOFormatError,
        'Duration years component must be positive.',
        range_check)

:code:`DURATION_PNM_LIMIT`::

  Limit('Invalid month duration string.',
        0, None, ISOFormatError,
        'Duration months component must be positive.',
        range_check)

:code:`DURATION_PNW_LIMIT`::

  Limit('Invalid week duration string.',
        0, None, ISOFormatError,
        'Duration weeks component must be positive.',
        range_check)

:code:`DURATION_PND_LIMIT`::

  Limit('Invalid day duration string.',
        0, None, ISOFormatError,
        'Duration days component must be positive.',
        range_check)

:code:`DURATION_TNH_LIMIT`::

  Limit('Invalid hour duration string.',
        0, None, ISOFormatError,
        'Duration hours component must be positive.',
        range_check)

:code:`DURATION_TNM_LIMIT`::

  Limit('Invalid minute duration string.',
        0, None, ISOFormatError,
        'Duration minutes component must be positive.',
        range_check)

:code:`DURATION_TNS_LIMIT`::

  Limit('Invalid second duration string.',
        0, None, ISOFormatError,
        'Duration seconds component must be positive.',
        range_check)


:code:`INTERVAL_RNN_LIMIT`::

  Limit('Invalid duration repetition string.',
        0, None, ISOFormatError,
        'Duration repetition count must be positive.',
        range_check)

Range dicts
-----------

The range check methods defined in the :code:`BaseTimeBuilder` take corresponding :code:`rangedict` arguments defined in :code:`BaseTimeBuilder`. Arguments without a matching :code:`rangedict` entry are not range checked (or cast). They are defined as follows:

:code:`DATE_RANGE_DICT`::

  {'YYYY': DATE_YYYY_LIMIT,
   'MM': DATE_MM_LIMIT,
   'DD': DATE_DD_LIMIT,
   'Www': DATE_WWW_LIMIT,
   'D': DATE_D_LIMIT,
   'DDD': DATE_DDD_LIMIT}

:code:`TIME_RANGE_DICT`::

  {'hh': TIME_HH_LIMIT,
   'mm': TIME_MM_LIMIT,
   'ss': TIME_SS_LIMIT}

:code:`DURATION_RANGE_DICT`::

  {'PnY': DURATION_PNY_LIMIT,
   'PnM': DURATION_PNM_LIMIT,
   'PnW': DURATION_PNW_LIMIT,
   'PnD': DURATION_PND_LIMIT,
   'TnH': DURATION_TNH_LIMIT,
   'TnM': DURATION_TNM_LIMIT,
   'TnS': DURATION_TNS_LIMIT}

:code:`REPEATING_INTERVAL_RANGE_DICT`::

  {'Rnn': INTERVAL_RNN_LIMIT}

:code:`TIMEZONE_RANGE_DICT`::

  {'hh': TZ_HH_LIMIT,
   'mm': TZ_MM_LIMIT}

Build methods
=============

Build methods are called at the end of a "successful" parse. They are called with the parse components as strings. The only guarantee is that the strings correspond to the location of the component in the ISO 8601 string, no range checking is performed. Helpers are provided for range checking and casting, see `Range check methods`_ for more details. Some parse components e.g. timezones, will be passed as named tuples as built by :code:`builders.TupleBuilder`, :code:`BaseTimeBuilder._build_object` is given as a helper method to go from a named tuple to an object by way of the class' defined build methods.

Build methods are expected to be class methods as no builder instantiation is done in the parse methods.

The return value should be the desired return value for the corresponding parse method, e.g. :code:`build_date` for the :code:`PythonTimeBuilder` returns a Python `date <https://docs.python.org/3/library/datetime.html#datetime.date>`_ object.

build_date
----------

:code:`YYYY` (:code:`str`, default: :code:`None`) - Year component
:code:`MM` (:code:`str`, default: :code:`None`) - Month component
:code:`DD` (:code:`str`, default: :code:`None`) - Day component
:code:`Www` (:code:`str`, default: :code:`None`) - `Week number <https://en.wikipedia.org/wiki/ISO_week_date>`_ component
:code:`D` (:code:`str`, default: :code:`None`) - Weekday number component
:code:`DDD` (:code:`str`, default: :code:`None`) - `Ordinal <https://en.wikipedia.org/wiki/Ordinal_date>`_ day of year component

build_time
----------

:code:`hh` (:code:`str`, default: :code:`None`) - Hour component
:code:`mm` (:code:`str`, default: :code:`None`) - Minute component
:code:`ss` (:code:`str`, default: :code:`None`) - Second component
:code:`tz` (:code:`TimezoneTuple`, default: :code:`None`) - Timezone component as named tuple

build_datetime
--------------

:code:`date` (:code:`DateTuple`, default :code:`None`) - Date component as named tuple
:code:`time` (:code:`TimeTuple`, default :code:`None`) - Time component as named tuple

build_duration
--------------

:code:`PnY` (:code:`str`, default: :code:`None`) - Year component
:code:`PnM` (:code:`str`, default: :code:`None`) - Month component
:code:`PnW` (:code:`str`, default: :code:`None`) - Week component
:code:`PnD` (:code:`str`, default: :code:`None`) - Day component
:code:`TnH` (:code:`str`, default: :code:`None`) - Hour component
:code:`TnM` (:code:`str`, default: :code:`None`) - Minute component
:code:`TnS` (:code:`str`, default: :code:`None`) - Second component

build_interval
--------------

:code:`start` (:code:`DateTuple`, :code:`DatetimeTuple`, default: :code:`None`) - Start component as named tuple
:code:`end` (:code:`DateTuple`, :code:`DatetimeTuple`, default: :code:`None`) - End component as named tuple
:code:`duration` (:code:`DurationTuple`, default: :code:`None`) - Duration component as named tuple

build_repeating_interval
------------------------

:code:`R` (:code:`boolean`, default: :code:`None`) - :code:`True` if interval repeats without bound, :code:`False` otherwise, default :code:`None` value should never be passed
:code:`Rnn` (:code:`str`, default: :code:`None`) - Repetition count component
:code:`interval` (:code:`IntervalTuple`, default: :code:`None`) - Interval component as a named tuple

build_timezone
--------------

:code:`negative` (:code:`boolean`, default: :code:`None`) - :code:`True` if UTC offset is negative, :code:`False` otherwise, default :code:`None` value should never be passed
:code:`Z` (:code:`boolean`, default: :code:`None`) - :code:`True` if the parsed timezone string is "Z" and the UTC offset should be 0, :code:`False` otherwise, default :code:`None` value should never be passed
:code:`hh` (:code:`str`, default: :code:`None`) - Hour component of UTC offset
:code:`mm` (:code:`str`, default: :code:`None`) - Minute component of UTC offset
:code:`name` (:code:`str`, default: :code:`''`) - Timezone name

Range check methods
===================

Every build method has a corresponding range check method, e.g. :code:`range_check_date` for :code:`build_date`. Range methods take the same arguments as their corresponding build method. Range methods are expected to cast the arguments to the correct type, range check them, and return the (now casted) arguments as a `tuple <https://docs.python.org/3/library/stdtypes.html#typesseq-tuple>`_ in the same order the method was called with. These methods are not called by default in the :code:`BaseTimeBuilder` or :code:`TupleBuilder` build methods.

The final argument to every range check method is a :code:`rangedict`. :code:`rangedict` is expected to be a `dictionary <https://docs.python.org/3/library/stdtypes.html#dict>`_ with keys matching the build method arguments, and values being corresponding :code:`aniso8601.builders.Limit` named tuples. The range check methods will by default use a matching range dict if no argument to :code:`rangedict` is provided, e.g. :code:`BaseTimeBuilder.DATE_RANGE_DICT` is used by default by :code:`BaseTimeBuilder.range_check_date`.

Note that there is no :code:`range_check_interval` method. Since the :code:`start`, :code:`end`, and :code:`duration` arguments are all different, already range checked types, it is assumed the build method will be calling range checked build methods internally (likely via :code:`_build_object`). An additional :code:`range_check_interval` method would be redundant. However a builder is welcome to implement one if necessary, :code:`PythonTimeBuilder` has additional range checking logic in :code:`range_check_duration` as well as a :code:`range_check_interval` method, both of which check against maximum Python timedelta size.

range_check_date
----------------

:code:`YYYY` (:code:`str`, default: :code:`None`) - Year component
:code:`MM` (:code:`str`, default: :code:`None`) - Month component
:code:`DD` (:code:`str`, default: :code:`None`) - Day component
:code:`Www` (:code:`str`, default: :code:`None`) - `Week number <https://en.wikipedia.org/wiki/ISO_week_date>`_ component
:code:`D` (:code:`str`, default: :code:`None`) - Weekday number component
:code:`DDD` (:code:`str`, default: :code:`None`) - `Ordinal <https://en.wikipedia.org/wiki/Ordinal_date>`_ day of year component
:code:`rangedict` (:code:`dict`, default: :code:`None`) - Dict with key of argument name, value of Limit named tuple to apply to the value

Returns - Tuple of values in same order as kwargs that have been cast and range checked

range_check_time
----------------

:code:`hh` (:code:`str`, default: :code:`None`) - Hour component
:code:`mm` (:code:`str`, default: :code:`None`) - Minute component
:code:`ss` (:code:`str`, default: :code:`None`) - Second component
:code:`tz` (:code:`TimezoneTuple`, default: :code:`None`) - Timezone component as named tuple
:code:`rangedict` (:code:`dict`, default: :code:`None`) - Dict with key of argument name, value of Limit named tuple to apply to the value

Returns - Tuple of values in same order as kwargs that have been cast and range checked

range_check_duration
--------------------

:code:`PnY` (:code:`str`, default: :code:`None`) - Year component
:code:`PnM` (:code:`str`, default: :code:`None`) - Month component
:code:`PnW` (:code:`str`, default: :code:`None`) - Week component
:code:`PnD` (:code:`str`, default: :code:`None`) - Day component
:code:`TnH` (:code:`str`, default: :code:`None`) - Hour component
:code:`TnM` (:code:`str`, default: :code:`None`) - Minute component
:code:`TnS` (:code:`str`, default: :code:`None`) - Second component
:code:`rangedict` (:code:`dict`, default: :code:`None`) - Dict with key of argument name, value of Limit named tuple to apply to the value

Returns - Tuple of values in same order as kwargs that have been cast and range checked

range_check_repeating_interval
------------------------------

:code:`R` (:code:`boolean`, default: :code:`None`) - :code:`True` if interval repeats without bound, :code:`False` otherwise, default :code:`None` value should never be passed
:code:`Rnn` (:code:`str`, default: :code:`None`) - Repetition count component
:code:`interval` (:code:`IntervalTuple`, default: :code:`None`) - Interval component as a named tuple
:code:`rangedict` (:code:`dict`, default: :code:`None`) - Dict with key of argument name, value of Limit named tuple to apply to the value

Returns - Tuple of values in same order as kwargs that have been cast and range checked

range_check_repeating_timezone
------------------------------

:code:`negative` (:code:`boolean`, default: :code:`None`) - :code:`True` if UTC offset is negative, :code:`False` otherwise, default :code:`None` value should never be passed
:code:`Z` (:code:`boolean`, default: :code:`None`) - :code:`True` if the parsed timezone string is "Z" and the UTC offset should be 0, :code:`False` otherwise, default :code:`None` value should never be passed
:code:`hh` (:code:`str`, default: :code:`None`) - Hour component of UTC offset
:code:`mm` (:code:`str`, default: :code:`None`) - Minute component of UTC offset
:code:`name` (:code:`str`, default: :code:`''`) - Timezone name
:code:`rangedict` (:code:`dict`, default: :code:`None`) - Dict with key of argument name, value of Limit named tuple to apply to the value

Returns - Tuple of values in same order as kwargs that have been cast and range checked

Helper class methods
====================

:code:`BaseTimeBuilder` has some convenience methods to help deal with intervals.

_is_interval_end_precise
------------------------

:code:`endtuple` (:code:`TimeTuple`, :code:`DateTuple`, :code:`DatetimeTuple`) - The :code:`end` member of an :code:`IntervalTuple` to check

Returns - :code:`True` if `endtuple` will take missing components from the :code:`start` of an :code:`IntervalTuple`, :code:`False` otherwise

_combine_concise_interval_tuples
--------------------------------

:code:`starttuple` (:code:`TimeTuple`, :code:`DateTuple`, :code:`DatetimeTuple`) - The :code:`start` member of an :code:`IntervalTuple`
:code:`conciseendtuple` (:code:`TimeTuple`, :code:`DateTuple`, :code:`DatetimeTuple`) - The :code:`end` member of an :code:`IntervalTuple` which will have missing components added from :code:`starttuple`

Returns - A :code:`DatetimeTuple` if :code:`start` is a :code:`DatetimeTuple` or :code:`conciseendtuple` is a :code:`DatetimeTuple` or :code:`TimeTuple`, a :code:`DateTuple` otherwise. Any components present in :code:`start` but missing in :code:`conciseendtuple` will be taken from :code:`start`.

Other methods
=============

There are a couple other common methods in :code:`builders`.

cast
----

:code:`builders.cast` used as a wrapper around cast methods to handle throwing the correct exception.

:code:`value` - The value to be cast
:code:`castfunction` (:code:`method`) - Method to call to cast :code:`value` to the desired return type
:code:`caughtexceptions` (:code:`iterable`, default: :code:`(ValueError,)`) - Iterable of the types of exceptions that should be caught when calling :code:`castfunction`
:code:`thrownexception` (:code:`Exception`, default: :code:`ISOFormatError`) - The exception to throw when one of :code:`caughtexceptions` is caught
:code:`thrownmessage` (:code:`str`, default: :code:`None`) - String passed to :code:`thrownexception` constructor

Returns - The output of :code:`castfunc` when called with :code:`value`

range_check
-----------

:code:`builders.range_check` is the range check method used by all :code:`BaseTimeBuilder` limits. If "." is present in :code:`valuestr`, it will be cast to :code:`float` (via :code:`builders.cast`), :code:`int` otherwise.

:code:`valuestr` (:code:`str`) - The value to cast and range check
:code:`limit` (:code:`Limit`) - The `Limit`_ tuple to use to range check

Returns - :code:`valuestr` if cast is successful and range checks pass
