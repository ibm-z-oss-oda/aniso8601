Changelog
=========

aniso8601 4.0.0dev0
===================

*Release date: YYYY-MM-DD*

Changes
-------
* All parse functions now take an optional :code:`builder` argument allowing for changing output format, :code:`PythonTimeBuilder` is used by default maintaining compatbility with previous versions (`discussion <https://bitbucket.org/nielsenb/aniso8601/issues/10/sub-microsecond-precision-in-durations-is#comment-47782063>`_)
* Custom error types, especially :code:`ISOFormatError` are raised for all known format errors (`issue 18 <https://bitbucket.org/nielsenb/aniso8601/issues/18/parsing-time-throw-a-valueerror-instead-of>`_)

Deprecation
-----------
* :code:`relative` keyword argument deprecated for all functions where it was available (:code:`parse_duration`, :code:`parse_interval`)
