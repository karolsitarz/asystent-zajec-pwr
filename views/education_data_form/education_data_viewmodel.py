import re
from typing import Union, Optional

from model.data.course import Course
from model.data.education_data import EducationData
from model.data.event import Event
from model.logic.observable import Observable
from model.repository import Repository
from util.constants import url_pattern
from util.constants import ViewName


class EducationDataViewModel:
    def __init__(self):
        self.errors: Observable[list[str]] = Observable([])
        self.selected = Repository.selected_education_data

    @staticmethod
    def action_cancel():
        Repository.active_view.value = ViewName.SINGLE_EVENT

    def action_submit(self, name: str, value: str, is_url: bool) -> bool:
        source: Union[Course, Event]
        education_data: Optional[EducationData]
        is_course: bool
        (source, education_data, is_course) = self.selected.value

        errors = []
        if len(name) == 0:
            errors.append("Nazwa nie może być pusta")
        if is_url and not re.match(url_pattern, value):
            errors.append("Zawartość nie jest linkiem")

        self.errors.value = errors
        if len(errors) > 0:
            return False

        # adding
        if education_data is None:
            new_education_data = EducationData(name, value, is_url)
            source.add_data(new_education_data)
        # editing
        else:
            education_data.update(name, value, is_url)

        self.selected.emit()
        Repository.selected_event.emit()
        Repository.has_changed.value = True
        Repository.active_view.value = ViewName.SINGLE_EVENT
        return True

    def action_delete(self):
        source: Union[Course, Event]
        education_data: Optional[EducationData]
        (source, education_data, _) = self.selected.value
        source.delete_data(education_data)

        Repository.selected_event.emit()
        Repository.has_changed.value = True
        Repository.active_view.value = ViewName.SINGLE_EVENT
