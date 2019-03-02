Changelog
=========

aniso8601 5.1.1dev0
===================

*Release date: YYYY-MM-DD*

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
