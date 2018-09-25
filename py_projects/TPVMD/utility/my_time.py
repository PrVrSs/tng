from datetime import datetime, timedelta


def to_second(time_):
    return datetime(year=time_[0], month=time_[1], day=time_[2],
                    hour=time_[3], minute=time_[4], second=time_[5], microsecond=1000*time_[6]).timestamp()


def from_second(second):
    return datetime.fromtimestamp(second)
