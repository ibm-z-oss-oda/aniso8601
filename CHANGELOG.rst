Changelog
=========

aniso8601 8.0.1-dev.0
=====================

*Release date: YYYY-MM-DD*

Changes
-------

* Empty and None date strings now raise :code:`ISOFormatError`, fixes `26 <https://bitbucket.org/nielsenb/aniso8601/issues/26/parse_date-parse_time-parse_datetime-fails>`_
* Empty and None duration strings now raise :code:`ISOFormatError`
* Empty and None interval strings now raise :code:`ISOFormatError`
* Empty and None time strings now raise :code:`ISOFormatError`

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
