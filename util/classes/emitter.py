from util.classes.observer import Observer


class Emitter:
    def __init__(self):
        self.__observers: set[Observer] = set()

    def add_observer(self, observer: Observer):
        self.__observers.add(observer)

    def emit(self, *data):
        for observer in self.__observers:
            observer.observe(*data)
