from typing import TypeVar, Generic, Callable

T = TypeVar('T')


class Observable(Generic[T]):
    def __init__(self, default_value: T = None):
        self.__value = default_value
        self.__observers: set[Callable[[T], None]] = set()

    def observe(self, callback: Callable[[T], None]):
        self.__observers.add(callback)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: T):
        self.__value = value
        self.emit()

    def emit(self):
        for callback in self.__observers:
            callback(self.__value)
