"""
Functions for parsing, formatting, and generating dates.
TODO:
    - [ ] Don'y use dateutil. it is evil but oh so tempting.
"""
# ///////////////////
# Imports
# ///////////////////

import pytz
import datetime
from datetime import datetime as DateTimeType
import logging
from typing import Callable, Union, NewType, List, Any, Set

from dateutil import parser


# ///////////////////
# Logger
# ///////////////////

DATE_LOGGER = logging.getLogger()

# ///////////////////
# Custom Types
# ///////////////////
DateTimeString = NewType("DateTimeString", Union[DateTimeType, str])
DateTimeStamp = NewType("DateTimeStamp", Union[str, int, float])

# ///////////////////
# Doc strings
# ///////////////////
DATE_PARAM = ":param date: datetime date to proccess. The default is `now()`"
DELTA_PARAMS = """
:param weeks: number of weeks 
:param days:  number of weeks 
:param minutes:  number of weeks 
:param seconds:  number of weeks 
:param microseconds:  number of weeks 
:param milliseconds:  number of weeks 
"""
STRING_PARAM = ":param string: A stirng as a date"


# ///////////////////
# Functions
# ///////////////////


def now() -> DateTimeType:
    """
    Generate the current, timezeone-aware UTC time
    """
    return DateTimeType.utcnow().replace(tzinfo=pytz.UTC)


DELTA_KWARGS = ["days", "seconds", "microseconds", "milliseconds", "minutes", "weeks"]


def delta(**kwargs) -> datetime.timedelta:
    f"""
    Generate a timedelta object.
    {DELTA_KWARGS}
    """
    return datetime.timedelta(**kwargs)


def before(date: DateTimeType = now(), **kwargs) -> DateTimeType:
    f"""
    Generate a date before a given `date`
    {DATE_PARAM}
    {DELTA_PARAMS}
    """
    return date - delta(**kwargs)


def after(date: DateTimeType = now(), **kwargs) -> DateTimeType:
    f"""
    Generate a date after a given `date`
    {DATE_PARAM}
    {DELTA_PARAMS}
    """
    return date + delta(**kwargs)


import string

DIGITS = frozenset(string.digits)


def _is_digit(text: str, digits: Union[List[str], Set[str]] = DIGITS) -> bool:
    f"""
    Return true if this text is a digits character
    :param text: The text to check against.
    :param digits: An optional list of digits characters check against
    :return bool
    """
    return text in digits


def _is_int(text: str, digits: Union[List[str], Set[str]] = DIGITS) -> bool:
    f"""
    Return true if this text is an integer (all characters are numeric)
    :param text: The text to check against.
    :param digits: An optional list of digits characters check against
    :return bool
    """
    return all([_is_digit(c, digits) for c in text])


def from_string(string: str, **kwargs) -> DateTimeType:
    f"""
    Convert a string into a  date.
    {STRING_PARAM}
    """
    if isinstance(string, DateTimeType):
        return string
    # overrides
    if _is_int(string):
        if len(string) == 4:
            return datetime.datetime(int(string), 1, 1, 0, 0, 0)
        elif len(string) < 9:
            return parser.parse(string, **kwargs)
        elif len(string) >= 9:
            return from_ts(string)
    return parser.parse(string, **kwargs)


def date_range(
    date: DateTimeType = now(),
    dir: str = "desc",
    unit: str = "days",
    num: int = 1,
    as_string: bool = False,
    to_string: Callable = lambda x: x.isoformat(),
) -> List[DateTimeString]:
    f"""
    Generate a range of dates
    {DATE_PARAM}
    :param dir: The direction to build the range, ``asc`` or ``desc``
    :param unit: The unit to increment the range by, either ``days``, ``weeks``, ``hours``, ``minutes``, ``seconds``
    :param num: The number of dates to generate
    :return list
    """
    if dir == "desc":
        fx = before
    else:
        fx = after
    dates = [fx(date, **{unit: x}) for x in range(num)]
    if as_string:
        return list(map(dates, to_string))
    return dates


def from_ts(timestamp: DateTimeStamp) -> DateTimeType:
    """
    :params timestamp: A UTC Timestamp, either ``int``, ``float``, or ``str``
    """
    return datetime.fromtimestamp(timestamp).replace(tzinfo=pytz.UTC)


def is_date(obj: Any) -> bool:
    """
    :params obj an object to test for a date type
    :reutnr bool
    """
    return isinstance(obj, (datetime.timedelta, datetime.datetime, datetime.date))


DATE_FIELD_NAMES = frozenset(
    [
        "created",
        "updated",
        "deleted",
        "created_at",
        "updated_at",
        "deleted_at",
        "file_modified_at",
    ]
)


def is_field_date(field_name: str) -> bool:
    """
    Heuristic-based testing to check if a field name contains dates
    :param field_name: A field / column name
    """
    if (
        field_name in DATE_FIELD_NAMES
        or field_name.endswith("_at")
        or field_name.endswith("_date")
        or "datetime" in field_name
        or "date_" in field_name
        or "_date" in field_name
    ):
        return True
    return False
