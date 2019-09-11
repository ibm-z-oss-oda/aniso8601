import re


_SIGN_PATTERN = re.compile(r'[,\.]')


def find_separator(value):
    """Returns the decimal separator index if found else -1."""
    match = _SIGN_PATTERN.search(value)
    if not match:
        return -1
    return match.start()


def normalize(value):
    """Returns the string that the decimal separators are normalized."""
    return _SIGN_PATTERN.sub('.', value)
