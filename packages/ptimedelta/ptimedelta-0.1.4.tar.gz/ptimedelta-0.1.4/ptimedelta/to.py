import datetime

from ptimedelta.six import string_types
from ptimedelta.regex import TIME_PERIOD_PATTERN
from ptimedelta.const import MS_IN_SEC


def to_timedelta(time_period):  # type (str) -> datetime.timedelta
    """
    Return the timedelta object derived from the string representation of a time period.

    >>> import ptimedelta as ptd
    >>> ptd.to_timedelta("10m")
    datetime.timedelta(seconds=600)
    >>> ptd.to_timedelta("43min")
    datetime.timedelta(seconds=2580)
    >>> ptd.to_timedelta("1m27s")
    datetime.timedelta(seconds=87)
    >>> ptd.to_timedelta("65sec")
    datetime.timedelta(seconds=65)
    >>> ptd.to_timedelta("3h2min")
    datetime.timedelta(seconds=10920)
    >>> ptd.to_timedelta("2d4s")
    datetime.timedelta(days=2, seconds=4)

    For Python2.7 unicode strings are also supported:

    >>> ptd.to_timedelta(u"3m2s")
    datetime.timedelta(seconds=182)

    Milliseconds are supported:

    >>> ptd.to_timedelta("3s56ms")
    datetime.timedelta(seconds=3, microseconds=56000)

    And float point values too:

    >>> ptd.to_timedelta("2.63ms")
    datetime.timedelta(microseconds=2630)
    """
    if not isinstance(time_period, string_types):
        raise TypeError(
            "Valid data type is string but %s is given." % type(time_period).__name__
        )

    if not time_period:
        raise ValueError("Empty string is an invalid time period.")

    matched = TIME_PERIOD_PATTERN.match(time_period)

    if matched:
        return datetime.timedelta(
            **{
                key: float(value)
                for key, value in matched.groupdict().items()
                if value is not None
            }
        )

    raise ValueError("Given string `%s` is an invalid time period." % time_period)


def to_seconds(time_period, as_int=False):  # type (str, bool) -> Union[int, float]
    """
    Convert a time period represented by a string to the number of seconds.

    :param time_period: Time period.
    :type time_period: str
    :param as_int: If equals to `True` the return value is casted to the integer.
    :type as_int: bool

    Examples:
    >>> import ptimedelta as ptd
    >>> ptd.to_seconds("56m29s")
    3389.0
    >>> ptd.to_seconds("0s", as_int=True)
    0
    >>> ptd.to_seconds("5s34ms")
    5.034
    """
    seconds = to_timedelta(time_period).total_seconds()

    if as_int:
        return int(seconds)
    else:
        return seconds


def to_milliseconds(time_period, as_int=False):  # type (str, bool) -> Union[int, float]
    """
    Convert a time period represented by a string to the number of milliseconds.

    :param time_period: Time period.
    :type time_period: str
    :param as_int: If equals to `True` the return value is casted to the integer.
    :type as_int: bool

    Examples:
    >>> import ptimedelta as ptd
    >>> ptd.to_milliseconds("12.64ms")
    12.64
    >>> ptd.to_milliseconds('3.1472s', as_int=True)
    3147
    """
    seconds = to_seconds(time_period, as_int=False)
    milliseconds = seconds * MS_IN_SEC

    if as_int:
        return int(milliseconds)
    else:
        return milliseconds
