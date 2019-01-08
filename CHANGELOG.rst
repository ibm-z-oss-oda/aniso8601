Changelog
=========

aniso8601 4.1.0dev0
===================

*Release date: YYYY-MM-DD*

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
