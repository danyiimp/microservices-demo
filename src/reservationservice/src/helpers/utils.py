from datetime import date, datetime, timedelta

from src.schemas.time_interval import TimeInterval
from src.core.config import settings


PT = settings.PAUSE_TIME_BEFORE_AND_AFTER_RESERVATION_IN_MIN


def get_awailable_time_intervals(
    date: date, busy_time: list[TimeInterval], pt: int = PT
) -> list[TimeInterval]:
    lb = datetime.combine(date, datetime.min.time())
    ub = datetime.combine(date, datetime.max.time())

    if busy_time == []:
        return [TimeInterval(time_start=lb, time_end=ub)]

    res = []

    if busy_time[0].time_start > lb:
        time_start = lb
        time_end = busy_time[0].time_start - timedelta(minutes=pt)
        if time_start < time_end:
            res.append(TimeInterval(time_start=time_start, time_end=time_end))

    for i in range(len(busy_time) - 1):
        time_start = busy_time[i].time_end + timedelta(minutes=pt)
        time_end = busy_time[i + 1].time_start - timedelta(minutes=pt)
        if time_start < time_end:
            res.append(TimeInterval(time_start=time_start, time_end=time_end))

    if busy_time[-1].time_end < ub:
        time_start = busy_time[-1].time_end + timedelta(minutes=pt)
        time_end = ub
        if time_start < time_end:
            res.append(TimeInterval(time_start=time_start, time_end=time_end))
    return res
