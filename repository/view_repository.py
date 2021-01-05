from util.classes.emitter import Emitter
from util.classes.singleton import Singleton
from util.constants.views import LOADING


class ViewRepository(Emitter, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.__active_view: str = LOADING

    def set_view(self, view: str):
        self.__active_view = view
        self.emit(self.__active_view)
