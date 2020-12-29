class CourseData:
    def __init__(self, name: str, value: str, is_url: bool):
        self.__name = name
        self.__value = value
        self.__is_url = is_url

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @property
    def is_url(self):
        return self.__is_url


class Course:
    def __init__(self, code: str, course_type: str, name: str, lecturer: str):
        self.__code = code
        self.__name = name
        self.__course_type = course_type
        self.__lecturer = lecturer
        self.__data: list[CourseData] = []

    @property
    def code(self):
        return self.__code

    @property
    def name(self):
        return self.__name

    @property
    def type(self):
        return self.__course_type

    @property
    def lecturer(self):
        return self.__lecturer

    def add_info(self, name: str, value: str, is_url: bool):
        self.__data.append(CourseData(name, value, is_url))

    def update_info(self, index: int, name: str, value: str, is_url: bool):
        info = self.__data[index]
        self.__data[index] = CourseData(name or info.name, value or info.value, is_url or info.is_url)

    def delete_info(self, index: int):
        self.__data.pop(index)

    @staticmethod
    def predicate(course: 'Course', course_type: str, name: str):
        return course.type == course_type and course.name == name


class Event:
    def __init__(self, start: str, end: str, location: str, code: str):
        self.__code = code
        self.__location = location
        self.__start = start
        self.__end = end

    @property
    def code(self):
        return self.__code

    @property
    def location(self):
        return self.__location

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end


class Repository:
    __courses: list[Course] = []
    __events: list[Event] = []

    @classmethod
    def is_empty(cls):
        return len(cls.__courses) == 0 or len(cls.__events) == 0

    @classmethod
    def set_courses(cls, items: list[Course]):
        cls.__courses = items

    @classmethod
    def set_events(cls, items: list[Event]):
        cls.__events = items
