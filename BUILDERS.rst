aniso8601 - Builder Development
===============================

Most builders will descend from either :code:`aniso8601.builders.BaseTimeBuilder` or :code:`aniso8601.builders.python.PythonTimeBuilder`.

Builder class variables
=======================

:code:`LEAP_SECONDS_SUPPORTED` (:code:`boolean`, default :code:`False`) - Set to :code:`True` if :code:`range_check_time` should accept `leap seconds <https://en.wikipedia.org/wiki/Leap_second>`_. Otherwise :code:`range_check_time` will raise a :code:`LeapSecondError` when range checking a time representing a leap second.

The limit variables will be discussed in the TODO.

Build methods
=============

Build methods are called at the end of a "successful" parse. They are called with the parse components as strings. The only guarantee is that the strings correspond to the location of the component in the ISO 8601 string, no range checking is performed. Helpers are provided for range checking and casting, see TODO for more details. Some parse components e.g. timezones, will be passed as named tuples as built by :code:`aniso8601.builders.TupleBuilder`, :code:`BaseTimeBuilder._build_object` is given as a helper method to go from a named tuple to an object by way of the class' defined build methods.

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
