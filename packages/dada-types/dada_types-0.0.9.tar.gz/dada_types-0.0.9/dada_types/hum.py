"""
Utilities for displaying data in a human-friendly format
TODO
    - [ ] Integrate these into our type library
"""
# ///////////////////
# Imports
# ///////////////////

from typing import Any

# ///////////////////
# Reusable Doc Strings
# ///////////////////

ROUND_TO_PARAM = ":param round_to: The number of decimal places to round to"

# ///////////////////
# Functions
# ///////////////////


def display_seconds(n_seconds, round_to=1):
    f"""
    Convert seconds to human-readable to minutes, hours, days, weeks, etc. (eg: ``64`` -> ``1.1 minutes``)
    :param n_seconds: The number of seconds to humanize
    {ROUND_TO_PARAM}
    :return str
    """
    if n_seconds <= 60:
        return f"{round(n_seconds, round_to)} secs"
    elif n_seconds <= 3600:
        return f"{round(n_seconds/60.0, round_to)} minutes"
    elif n_seconds <= 3600 * 24:
        return f"{round(n_seconds/3600.0, round_to)} hours"
    elif n_seconds <= 3600 * 24 * 7:
        return f"{round(n_seconds/(3600.0  * 24), round_to)} days"
    return f"{round(n_seconds/(3600.0 * 24 * 7), round_to)} weeks"


def display_byte_size(filebytes, round_to=3):
    f"""
    Convert bytes to human-readable size, hours, days, weeks, etc. (eg: ``1024`` -> ``1.0 MB``)
    :param filebytes: The number of bytes to humanize
    {ROUND_TO_PARAM}
    :return str
    """
    for x in ["bytes", "KB", "MB", "GB", "TB"]:
        if filebytes < 1024.0:
            return "%3.1f %s" % (round(filebytes, round_to), x)
        filebytes /= 1024.0
