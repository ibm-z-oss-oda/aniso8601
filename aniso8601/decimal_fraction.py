import re


_SIGN_PATTERN = re.compile(r'[,\.]')


def find_sign(value):
    """Returns the sign index if found else -1."""
    match = _SIGN_PATTERN.search(value)
    if not match:
        return -1
    return match.start()


def has_sign(value):
    return find_sign(value) != -1


def split(value):
    """Returns the list spearated with decimal fraction signs."""
    return _SIGN_PATTERN.split(value)
