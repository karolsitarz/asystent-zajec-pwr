from model.data.course_data import CourseData


class Course:
    def __init__(self, code: str, course_type: str, name: str, lecturer: str):
        self.__code = code
        self.__name = name
        self.__course_type = course_type
        self.__lecturer = lecturer
        self.__data: list[CourseData] = []
        self.__is_hidden: bool = False

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

    @property
    def is_hidden(self):
        return self.__is_hidden

    def toggle_hidden(self):
        self.__is_hidden = not self.__is_hidden

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

    def to_dict(self):
        return {
            "code": self.__code,
            "name": self.__name,
            "course_type": self.__course_type,
            "lecturer": self.__lecturer,
            "data": self.__data,
            "is_hidden": self.__is_hidden,
        }

    @classmethod
    def from_dict(cls, data):
        obj = Course(data["code"], data["course_type"], data["name"], data["lecturer"])
        obj.__data = data["data"]
        obj.__is_hidden = data["is_hidden"]
        return obj
