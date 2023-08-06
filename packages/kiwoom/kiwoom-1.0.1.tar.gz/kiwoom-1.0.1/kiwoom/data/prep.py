from collections import defaultdict


"""
Default configuration of how to pre-process raw inputs from the server.
Default way to deal with data is considering one as a string.  

1) number
    : returns an int or a float

2) string
    : returns a string with white space removed

3) remove_sign (special case)
    : returns a number/string without any signs (+/-)
"""


def number(x):
    """
    First, tries to type-cast x into int. If it fails, move on to float.
    If converting to float raises an ValueError, then throws the error.
    """
    try:
        return int(x)
    except ValueError:
        pass
    try:
        return float(x)
    except ValueError:
        raise ValueError(f"{x} of Type {type(x)} can't be a number.")


def string(x):
    """
    Returns a string with white space removed.
    """
    return x.strip()


def remove_sign(x):
    """
    Returns number or string with '+' and '-' signs removed.

    1) Removes '+' or '-' from x
    2) Tries to type-cast x into number(int / float)
    3) If step number 2 fails, returns string.
    """
    x = x.translate({ord('+'): '', ord('-'): ''})
    try:
        x = number(x)
    except ValueError:
        x = string(x)
    return x


def prep(x):
    """
    Pre-process x into number or string

    :param x: str
    :return: int/float/str
    """
    try:
        return number(x)
    except ValueError:
        return string(x)
