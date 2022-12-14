Changelog
#########

aniso8601 9.0.2-dev.0
=====================

*Release date: YYYY-MM-DD*

aniso8601 9.0.1
===============

*Release date: 2021-03-01*

Added
-----
* Development requirements handled by :code:`extras_require` (install with :code:`pip install -e .[dev]`)
* Pre-commit hooks, managed with `pre-commit <https://pre-commit.com/>`_ (install with :code:`pre-commit install`)
* Add :code:`readthedocs.yaml` to make configuration explicit

Changed
-------
* Code formatted with `Black <https://black.readthedocs.io/en/stable/index.html>`_
* Imports sorted with `isort <https://pycqa.github.io/isort/>`_
* Following `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_ for this and future CHANGELOG entries
* Removed python-dateutil from :code:`BuildRequires` in specfile as they are no longer required since calendar level duration building was split to a separate project (6.0.0)
* Heading level of top of CHANGELOG

Fixed
-----
* Parsing prescribed durations with only hour and second time components (see `PR 14 <https://bitbucket.org/nielsenb/aniso8601/pull-requests/14>`_)
* Parsing prescribed durations with only year and day components

aniso8601 9.0.0
===============

*Release date: 2021-02-18*

Changes
-------
* Add support for concise interval format (see `27 <https://bitbucket.org/nielsenb/aniso8601/issues/27/support-for-short-syntax-for-intervals>`_)
* Add explicit bounds of [000, 366] to day of year component :code:`_parse_ordinal_date`, this adds the same limits to dates of the format YYYYDDD or YYYY-DDD when using :code:`parse_date`
* Add :code:`range_check_date`, :code:`range_check_time`, :code:`range_check_duration`, :code:`range_check_repeating_interval`, and :code:`range_check_timezone` range checking class methods to :code:`BaseTimeBuilder` there are no datetime or non-repeating interval check function as they are made of already checked parts
* :code:`PythonTimeBuilder` now calls the appropriate range check functions using the :code:`range_check_date`, :code:`range_check_time`, :code:`range_check_duration`, :code:`range_check_repeating_interval`, and :code:`range_check_timezone` methods defined in :code:`aniso8601.builders`
* Add :code:`range_check_duration` to :code:`PythonTimeBuilder` which calls :code:`BaseTimeBuilder.range_check_duration` and performs additional checks against maximum timedelta size
* Add :code:`range_check_interval` to :code:`PythonTimeBuilder` which handles building concise dates and performs additional checks against maximum timedelta size
* Add :code:`get_datetime_resolution` which behaves like :code:`get_time_resolution` but accepts a ISO 8601 date time as an argument, return value is a :code:`TimeResolution`
* Add :code:`exceptions.RangeCheckError` as a parent type of all failures in the range check methods, it descends from :code:`ValueError`
* Add :code:`get_duration_resolution` which behaves like other resolution helpers, return value is a :code:`DurationResolution`
* Add :code:`get_interval_resolution` which behaves like other resolution helpers, return value is a :code:`IntervalResolution`
* Negative durations now fail at the parse step and simply raise :code:`ISOFormatError`, calling a :code:`PythonTimeBuilder.build_duration` directly with a negative duration component will yield an :code:`ISOFormatError` in the range check
* Raise :code:`DayOutOfBoundsError` if calendar day exceeds number of days in calendar month
* Raise :code:`DayOutOfBoundsError` if ordinal day exceeds number of days in calendar year (366 now raises :code:`DayOutOfBoundsError` in non-leap year)
* Raise :code:`ISOFormatError` when date or time string contains extra whitespace
* Raise :code:`ISOFormatError` on multiple fraction separators (comma, full-stop) in a time string
* Raise :code:`ISOFormatError` when duration contains multiple duration designators ("P"), or time designators ("T")
* :code:`PythonTimeBuilder.build_duration` raises :code:`YearOutOfBoundsError`, :code:`MonthOutOfBoundsError`, :code:`WeekOutOfBoundsError`, :code:`HoursOutOfBoundsError`, :code:`MinutesOutOfBoundsError`, or :code:`SecondsOutOfBoundsError` when a given duration component would result in a :code:`timedelta` that would exceed the maximum size
* Raise :code:`ISOFormatError` if number of delimiters is not exactly 1 in :code:`parse_interval`
* Raise :code:`ISOFormatError` when either part of an interval string before of after the delimiter is empty
* Raise :code:`YearOutOfBoundsError` in :code:`PythonTimeBuilder.build_interval` if an interval with a duration would exceed the maximum or minimum years for Python date objects
* Simplify :code:`parse_date`, :code:`build_date` will now be called with explicit :code:`None` arguments instead of date components not in the parsed string excluded from the call
* Change :code:`get_date_resolution` to call :code:`parse_date` and return the resolution based on the smallest parsed component
* Simplify :code:`parse_time`, :code:`build_time` will now be called with explicit :code:`None` arguments instead of date components not in the parsed string excluded from the call
* Change :code:`get_time_resolution` to call :code:`parse_time` and return the resolution based on the smallest parsed component
* :code:`TupleBuilder` now builds :code:`DateTuple`, :code:`TimeTuple`, :code:`DatetimeTuple`, :code:`DurationTuple`, :code:`IntervalTuple`, :code:`RepeatingIntervalTuple` and :code:`TimezoneTuple` namedtuples
* Simplify :code:`parse_duration`, :code:`build_duration` will now be called with explicit :code:`None` arguments when components of a prescribed duration are not present in the ISO 8601 duration string instead of being excluded from the call
* Remove unused :code:`decimalfraction.find_separator`
* Remove unused :code:`PythonTimeBuilder._split_to_microseconds`
* Removed :code:`NegativeDurationError`

Deprecation
-----------
* **Update on Python 2 support**: Python 2 support was slated to be removed in 7.0.0 but was not, it will remain until a test fails on Python 2 but not Python 3
* Using Setuptools to run tests (:code:`python setup.py tests`) will be removed in the next major or minor version (either 9.1.0, 10.0.0)

aniso8601 8.1.1
===============

*Release date: 2021-01-29*

Changes
-------
* Add version to :code:`__init__.py`
* Cleaner reading of `README.rst` into the :code:`long_description` field of `setup.py`
* Define :code:`long_description_content_type` as :code:`text/x-rst`
* Simplify Sphinx configuration
* Add :code:`compat.is_string` method, returns :code:`True` for :code:`str`, :code:`unicode` types, :code:`False` otherwise, used to fix `28 <https://bitbucket.org/nielsenb/aniso8601/issues/28/810-breaks-parsing-unicode-strings-with>`_

Deprecation
-----------
* Deprecate running tests with :code:`python setup.py tests` as the test suite support in Setuptools is `deprecated <https://github.com/pypa/setuptools/issues/1684>`_

aniso8601 8.1.0
===============

*Release date: 2020-11-30*

Changes
-------
* Empty string arguments to :code:`get_date_resolution` and :code:`parse_date` now raise :code:`ISOFormatError`, fixes `26 <https://bitbucket.org/nielsenb/aniso8601/issues/26/parse_date-parse_time-parse_datetime-fails>`_
* None and non-string arguments to :code:`get_date_resolution` and :code:`parse_date` now raise :code:`ValueError`
* Empty string arguments to :code:`parse_duration` now raise :code:`ISOFormatError`
* None and non-string arguments to :code:`parse_duration` now raise :code:`ValueError`
* Empty string arguments to :code:`parse_interval` and :code:`parse_repeating_interval` now raise :code:`ISOFormatError`
* None and non-string arguments to :code:`parse_interval` and :code:`parse_repeating_internval` now raise :code:`ValueError`
* Empty string arguments to :code:`get_time_resolution` and :code:`parse_time` now raise :code:`ISOFormatError`
* None and non-string arguments to :code:`parse_time` now raise :code:`ValueError`
* None and non-string arguments to :code:`parse_timezone` now raise :code:`ValueError`
* Empty string arguments to :code:`parse_datetime` now raise :code:`ISOFormatError`
* None and non-string arguments to :code:`parse_datetime` now raise :code:`ValueError`
* Missing delimiter in datetime strings when calling :code:`parse_datetime` now raises :code:`ISOFormatError`
* Missing delimiter in regular and repeating interval strings when calling :code:`parse_interval` and :code:`parse_repeating_interval` now raises :code:`ISOFormatError`
* :code:`get_time_resolution` now correctly throws :code:`ISOFormatError` when a time component has too many characters in a time using ":" as a separator

aniso8601 8.0.0
===============

*Release date: 2019-09-11*

Changes
-------

* Handle ',' character as a fractional separator, as required by 4.2.2.4, see `PR 12 <https://bitbucket.org/nielsenb/aniso8601/pull-requests/12/allow-commas-as-decimal-separators-on-time/>`_
* Fix semver usage for prelease version, as required by `clause 9 <https://semver.org/#spec-item-9>`_

aniso8601 7.0.0
===============

*Release date: 2019-06-11*

Changes
-------
* Handle all fractional components as an integer number of microseconds, eliminating rounding issues, fixes `#24 <https://bitbucket.org/nielsenb/aniso8601/issues/24/float-induced-rounding-errors-when-parsing>`_

aniso8601 6.0.0
===============

*Release date: 2019-03-08*

Changes
-------
* Remove previously deprecated built in version of `relativetimebuilder <https://pypi.org/project/relativetimebuilder/>`_

Deprecation
-----------
* Python 2 support will be removed in 7.0.0

aniso8601 5.1.0
===============

*Release date: 2019-03-01*

Changes
-------
* Add `relativetimebuilder <https://pypi.org/project/relativetimebuilder/>`_ as an explicit requirement

aniso8601 5.0.1
===============

*Release date: 2019-03-01*

Changes
-------
* Make `python-dateutil <https://pypi.python.org/pypi/python-dateutil>`_ dependency explicit

aniso8601 5.0.0
===============

*Release date: 2019-03-01*

Changes
-------
* Previously deprecated :code:`relative` keyword removed
* Move builders to :code:`builders` module

  - :code:`aniso8601.builder.PythonTimeBuilder` -> :code:`aniso8601.builders.python.PythonTimeBuilder`
  - :code:`aniso8601.builder.RelativeTimeBuilder` -> :code:`aniso8601.builders.relative.RelativeTimeBuilder`
  - :code:`aniso8601.builder.TupleBuilder` -> :code:`aniso8601.builders.TupleBuilder`

* :code:`UTCOffset` moved out of :code:`builder` (:code:`aniso8601.builder.UTCOffset` -> :code:`aniso8601.utcoffset.UTCOffset`)
* Fractional arguments are now handled with greater precision (`discussion <https://bitbucket.org/nielsenb/aniso8601/issues/21/sub-microsecond-precision-is-lost-when>_`)
* When :code:`build_time` is called with only :code:`hh` 24<=hh<25, a :code:`MidnightBoundsError` is raised, this used to be a :code:`HoursOutOfBoundsError`
* Promote interval components to :code:`datetime` objects if the given duration has second or microsecond resolution, or if the duration tuple has hour, minute, or second components

  - Before promotion would only happen if the duration tuple had hour, minute, or second components

Deprecation
-----------
* The built in :code:`RelativeTimeBuilder` is deprecated, it will be removed in aniso8601 6.0.0, use :code:`RelativeTimeBuilder` from `relativetimebuilder <https://pypi.org/project/relativetimebuilder/>`_ instead

aniso8601 4.1.0
===============

*Release date: 2019-01-08*

Changes
-------
* Update copyright date
* Drop support for distutils
* Make tests package importable
* Add support for running tests via setuptools (:code:`python setup.py test`)
* Explicitly exclude .pyc, __pycache__ from bundles
* Use :code:`unittest.mock` with Python 3

aniso8601 4.0.1
===============

*Release date: 2018-10-25*

Changes
-------
* Correct date in CHANGELOG

aniso8601 4.0.0
===============

*Release date: 2018-10-25*

Changes
-------
* All parse functions now take an optional :code:`builder` argument allowing for changing output format, :code:`PythonTimeBuilder` is used by default maintaining compatbility with previous versions (`discussion <https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is#comment-47782063>`_)
* Custom error types, especially :code:`ISOFormatError` are raised for all known format errors (`issue 18 <https://bitbucket.org/nielsenb/aniso8601/issues/18/parsing-time-throw-a-valueerror-instead-of>`_)

Deprecation
-----------
* :code:`relative` keyword argument deprecated for all functions where it was available (:code:`parse_duration`, :code:`parse_interval`), it will be removed in aniso8601 5.0.0
