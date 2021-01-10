from datetime import datetime
from math import floor
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

    def __str__(self):
        return self.get_datetime().strftime("%d.%m.%Y %H:%M")

    def humanize(self):
        now = datetime.now().astimezone()
        delta = self.get_datetime() - now

        def print_absolute(value, unit):
            if value < 0:
                return f"{abs(floor(value))} {unit} temu"
            return f"za {floor(value)} {unit}"

        if delta.days == 0:
            if 0 <= delta.seconds / 60 <= 1:
                return "za chwilę"

            if 0 > delta.seconds / 60 >= -1:
                return "chwilę temu"

            if abs(delta.seconds) / 60 / 60 < 1:
                return print_absolute(delta.seconds / 60, "minut")

            return print_absolute(delta.seconds / 60 / 60, "godzin")

        return print_absolute(delta.days, "dni")
