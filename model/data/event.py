from model.data.course import Course
from model.data.education_data import EducationDataContainer
from model.data.datetime_epoch import DatetimeEpoch


class Event(EducationDataContainer):
    def __init__(self, start: DatetimeEpoch, end: DatetimeEpoch, location: str, course: Course):
        super().__init__()
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

    def to_dict(self):
        return {
            "course": self.__course.code,
            "location": self.__location,
            "start": self.__start.epoch,
            "end": self.__end.epoch,
            "data": self.list_to_json(),
        }

    @classmethod
    def from_dict(cls, data, course_list: list[Course]):
        course = next((c for c in course_list if c.code == data["course"]), None)
        start = DatetimeEpoch(data["start"])
        end = DatetimeEpoch(data["end"])
        obj = Event(start, end, data["location"], course)
        obj.list_from_json(data["data"])
        return obj
