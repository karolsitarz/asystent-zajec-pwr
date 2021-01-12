from datetime import datetime
from math import ceil
from zoneinfo import ZoneInfo

TIME_UNITS = {
    "NOW": ["chwilę", "chwile", "chwil"],
    "D": ["dzień", "dni", "dni"],
    "H": ["godzinę", "godziny", "godzin"],
    "M": ["minutę", "minuty", "minut"],
}


class DatetimeEpoch:
    def __init__(self, epoch: float):
        self.__epoch = epoch

    @classmethod
    def from_ical(cls, value: str):
        epoch = datetime.strptime(value[:15], "%Y%m%dT%H%M%S").timestamp()
        return DatetimeEpoch(epoch)

    def get_datetime(self):
        return datetime.fromtimestamp(self.__epoch).replace(tzinfo=ZoneInfo('UTC')).astimezone()

    @staticmethod
    def now_tz():
        return datetime.now().astimezone()

    @property
    def epoch(self):
        return self.__epoch

    def __str__(self):
        return self.get_datetime().strftime("%d.%m.%Y %H:%M")

    def humanize(self):
        now = DatetimeEpoch.now_tz()
        this = self.get_datetime()
        is_past = this < now
        delta = now - this if is_past else this - now

        def print_absolute(value, unit):
            print(value)
            string_builder = []
            corrected_value = value and ceil(value)
            if value is not None:
                string_builder.append(corrected_value.__str__())

            formatted_unit: str
            if value is None or corrected_value <= 1:
                formatted_unit = TIME_UNITS[unit][0]
            elif not (12 <= corrected_value <= 14) and 2 <= corrected_value % 10 <= 4:
                formatted_unit = TIME_UNITS[unit][1]
            else:
                formatted_unit = TIME_UNITS[unit][2]

            string_builder.append(formatted_unit)
            if is_past:
                string_builder.append("temu")
            else:
                string_builder.insert(0, "za")

            return " ".join(string_builder)

        if delta.days == 0:
            if delta.seconds / 60 <= 1:
                return print_absolute(None, "NOW")

            if abs(delta.seconds) / 60 / 60 < 1:
                return print_absolute(delta.seconds / 60, "M")

            return print_absolute(delta.seconds / 60 / 60, "H")

        return print_absolute(delta.days, "D")
