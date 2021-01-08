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
        self.events: Observable[list[tuple[bool, Event]]] = Observable()
        self.has_changed = Repository.has_changed

        def observe_events(events: list[Event]):
            self.update_events(events)

        Repository.events.observe(observe_events)
        Repository.courses.observe(lambda _: self.update_events(Repository.events.value))

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
        self.update_events(Repository.events.value)

    @staticmethod
    def navigate_to_course_list():
        Repository.active_view.value = ViewName.COURSE_LIST

    @staticmethod
    def on_event_selected(event):
        def action(_):
            Repository.selected_event.value = event
            Repository.active_view.value = ViewName.SINGLE_EVENT

        return action
