aniso8601 - Builder Development
===============================

Most builders will descend from either :code:`aniso8601.builders.BaseTimeBuilder` or :code:`aniso8601.builders.python.PythonTimeBuilder`.

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
:code:`interval` (:code:`IntervalTuple`, default: :code:`None`) - Interval component as a nemd tuple

build_timezone
--------------

:code:`negative` (:code:`boolean`, default: :code:`None`) - :code:`True` if UTC offset is negative, :code:`False` otherwise, default :code:`None` value should never be passed
:code:`Z` (:code:`boolean`, default: :code:`None`) - :code:`True` if the parsed timezone string is "Z" and the UTC offset should be 0, :code:`False` otherwise, default :code:`None` value should never be passed
:code:`hh` (:code:`str`, default: :code:`None`) - Hour component of UTC offset
:code:`mm` (:code:`str`, default: :code:`None`) - Minute component of UTC offset
:code:`name` (:code:`str`, default: :code:`''`) - Timezone name
