from typing import Union

from model.data.course import Course
from model.data.event import Event
from model.repository import Repository
from util.constants.views import ViewName


class SingleEventViewModel:
    def __init__(self):
        super().__init__()
        self.event = Repository.selected_event

    @staticmethod
    def go_back():
        Repository.active_view.value = ViewName.EVENT_LIST

    @staticmethod
    def add_education_data(source: Union[Course, Event], is_course: bool):
        Repository.selected_education_data.value = (source, None, is_course)
        Repository.active_view.value = ViewName.EDUCATION_DATA_FORM
