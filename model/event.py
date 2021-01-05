
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