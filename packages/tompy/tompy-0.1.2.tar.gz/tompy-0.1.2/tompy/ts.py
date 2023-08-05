import datetime


def date(year: int, month: int, day: int) -> datetime.date:
    return datetime.date(year, month, day)


def date_today() -> datetime.date:
    """
    Return the current local date.
    """
    return datetime.date.today()


def date_add(d: datetime.date, days: int) -> datetime.date:
    """
    days range: -999999999 <= days <= 999999999
    """
    return d + datetime.timedelta(days=days)


def date_weekday(d: datetime.date) -> int:
    """
    Return the day of the week as an integer, Monday is 0 and Sunday is 6.
    """
    return d.weekday()


def date_str(d: datetime.date) -> str:
    """
    Return a string representing the date in ISO 8601 format, YYYY-MM-DD.
    """
    return d.isoformat()


def date_from_str(datestr: str, fmt: str = "%Y-%m-%d") -> datetime.date:
    return datetime_from_str(datestr, fmt=fmt).date()


def datetime_today() -> datetime.datetime:
    """
    Return the current local datetime.
    """
    return datetime.datetime.today()


def datetime_from_str(
    datestr: str, fmt: str = "%Y-%m-%d"
) -> datetime.datetime:
    return datetime.datetime.strptime(datestr, fmt)
