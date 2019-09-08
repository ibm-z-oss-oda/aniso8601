import re


_SIGN_PATTERN = re.compile(r'[,\.]')


def find_separator(value):
    """Returns the decimal separator index if found else -1."""
    match = _SIGN_PATTERN.search(value)
    if not match:
        return -1
    return match.start()


def has_separator(value):
    return find_separator(value) != -1


def split(value):
    """Returns the list spearated with decimal separators."""
    return _SIGN_PATTERN.split(value)
