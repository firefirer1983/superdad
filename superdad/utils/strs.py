import datetime

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
DAY_FORMAT = "%Y-%m-%d"


def datetime_to_str(dt: datetime.datetime) -> str:
    return datetime.datetime.strftime(dt, DATETIME_FORMAT)


def datetime_to_day_str(dt: datetime.datetime) -> str:
    return datetime.datetime.strftime(dt, DAY_FORMAT)


def str_to_datetime(st: str) -> datetime.datetime:
    return datetime.datetime.strptime(st, DATETIME_FORMAT)


def day_str_to_datetime(st: str) -> datetime.datetime:
    return datetime.datetime.strptime(st, DAY_FORMAT)


def tomorrow_in_str(d):
    if isinstance(d, str):
        d = day_str_to_datetime(d)
    
    d += datetime.timedelta(days=1)
    d = datetime_to_day_str(d)
    return d


def truncate_by_day(dt: datetime.datetime) -> datetime.datetime:
    return day_str_to_datetime(datetime_to_day_str(dt))
