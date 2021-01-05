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
