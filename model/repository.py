class CourseData:
    def __init__(self, name, value, is_url):
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
    def __init__(self, code, course_type, name, lecturer):
        self.__code = code
        self.__name = name
        self.__course_type = course_type
        self.__lecturer = lecturer
        self.__data = []

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

    def add_info(self, name, value, is_url):
        self.__data.append(CourseData(name, value, is_url))

    def edit_info(self, index, name, value, is_url):
        self.__data[index] = CourseData(name, value, is_url)

    def delete_info(self, index):
        self.__data.pop(index)


# class Repository:
