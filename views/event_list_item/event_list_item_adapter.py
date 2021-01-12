from model.data.datetime_epoch import DatetimeEpoch
from model.data.event import Event
from model.logic.observable import Observable
from model.repository import Repository


class EventListItemAdapter:
    def __init__(self, event: Event):
        self.__event = event
        self.time_string: Observable[str] = Observable(self.__generate_time_string())

        def action(_):
            new_string = self.__generate_time_string()
            if self.time_string.value != new_string:
                self.time_string.value = new_string

        Repository.timer.observe(action)

    def __generate_time_string(self):
        now = DatetimeEpoch.now_tz()
        if now < self.__event.start.get_datetime():
            return self.__event.start.humanize()
        if now > self.__event.end.get_datetime():
            return self.__event.end.humanize()
        else:
            return f"w trakcie, koniec {self.__event.end.humanize()}"

