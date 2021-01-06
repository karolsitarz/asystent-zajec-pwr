from model.course import Course
from model.event import Event
from util.classes.observable import Observable
from util.classes.singleton import Singleton


class DataRepository(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.courses: Observable[list[Course]] = Observable([])
        self.events: Observable[list[Event]] = Observable([])

    def is_empty(self):
        return len(self.courses.value) == 0 or len(self.events.value) == 0

    def set_events(self, events: list[Event]):
        self.events.value = events

    def set_courses(self, courses: list[Course]):
        self.courses.value = courses
