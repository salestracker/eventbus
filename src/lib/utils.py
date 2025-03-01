import datetime as dt
import zoneinfo


def datetime_now() -> dt.datetime:
    return dt.datetime.now(zoneinfo.ZoneInfo("UTC"))


def to_timestamp(dtime: dt.datetime) -> float:
    return dtime.timestamp()
