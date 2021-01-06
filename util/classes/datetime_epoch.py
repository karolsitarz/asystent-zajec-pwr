from datetime import datetime
from zoneinfo import ZoneInfo


class DatetimeEpoch:
    def __init__(self, epoch: float):
        self.__epoch = epoch

    @classmethod
    def from_ical(cls, value: str):
        epoch = datetime.strptime(value[:15], "%Y%m%dT%H%M%S").timestamp()
        return DatetimeEpoch(epoch)

    def get_datetime(self):
        return datetime.fromtimestamp(self.__epoch).replace(tzinfo=ZoneInfo('UTC')).astimezone()

    @property
    def epoch(self):
        return self.__epoch
