from datetime import datetime
from typing import Optional

from model.data.event import Event
from model.logic.observable import Observable
from model.repository import Repository
from util.constants.views import ViewName


class SingleEventViewModel:
    def __init__(self):
        super().__init__()
        self.event = Repository.selected_event

    @staticmethod
    def go_back():
        Repository.active_view.value = ViewName.EVENT_LIST
