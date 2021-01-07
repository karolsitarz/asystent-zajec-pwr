from datetime import datetime
from typing import Optional

from model.data.event import Event
from model.logic.observable import Observable
from model.repository import Repository
from util.constants.views import ViewName


class EventListViewModel:
    def __init__(self):
        super().__init__()
        self.is_showing_all = False
        self.__events: Optional[list[Event]] = None
        self.events: Observable[list[tuple[bool, Event]]] = Observable()

        def observe_events(events: list[Event]):
            self.__events = events
            self.update_events(events)

        Repository.events.observe(observe_events)

    def update_events(self, events: list[Event]):
        now = datetime.now().astimezone()
        new_events = []

        for event in events:
            if event.course.is_hidden:
                continue

            is_before = event.start.get_datetime() < now
            if not self.is_showing_all and is_before:
                continue

            new_events.append((is_before, event))

        self.events.value = new_events

    def toggle_is_showing_all(self):
        self.is_showing_all = not self.is_showing_all
        self.update_events(self.__events)

    @staticmethod
    def on_event_selected(event):
        def action(_):
            Repository.selected_event.value = event
            Repository.active_view.value = ViewName.SINGLE_EVENT

        return action
