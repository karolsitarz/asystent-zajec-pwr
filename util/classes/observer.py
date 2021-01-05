from abc import abstractmethod, ABC


class Observer(ABC):
    @abstractmethod
    def observe(self, *data):
        pass
