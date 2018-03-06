class YearOutOfBoundsError(ValueError):
    """Raised when year exceeds limits."""

class WeekOutOfBoundsError(ValueError):
    """Raised when week exceeds a year."""

class DayOutOfBoundsError(ValueError):
    """Raised when day is outside of 1..365, 1..366 for leap year."""

class HoursOutOfBoundsError(ValueError):
    """Raise when parsed hours are greater than 24."""

class MinutesOutOfBoundsError(ValueError):
    """Raise when parsed seconds are greater than 60."""

class SecondsOutOfBoundsError(ValueError):
    """Raise when parsed seconds are greater than 60."""

class MidnightBoundsError(ValueError):
    """Raise when parsed time has an hour of 24 but is not midnight."""

class LeapSecondError(NotImplementedError):
    """Raised when attempting to parse a leap second"""
