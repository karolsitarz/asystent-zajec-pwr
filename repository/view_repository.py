from util.classes.observable import Observable
from util.classes.singleton import Singleton
from util.constants.views import LOADING


class ViewRepository(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.active_view = Observable(LOADING)
