from model.course import Course
from model.event import Event
from repository.view_repository import ViewRepository
from util.classes.emitter import Emitter
from util.classes.singleton import Singleton
from util.constants.views import LOGIN


class DataRepository(Emitter, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.__courses: list[Course] = []
        self.__events: list[Event] = []

    def is_empty(self):
        return len(self.__courses) == 0 or len(self.__events) == 0

    def set_data(self, courses: list[Course], events: list[Event]):
        self.__courses = courses
        self.__events = events
        self.emit(courses, events)

    def load_data(self):
        if DataRepository().is_empty():
            ViewRepository().set_view(LOGIN)
