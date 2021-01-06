from datetime import datetime

from model.course import Course


class Event:
    def __init__(self, start: datetime, end: datetime, location: str, course: Course):
        self.__course = course
        self.__location = location
        self.__start = start
        self.__end = end

    @property
    def course(self):
        return self.__course

    @property
    def location(self):
        return self.__location

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end
