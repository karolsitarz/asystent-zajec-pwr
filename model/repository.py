from typing import Optional, Union, Tuple

from model.data.course import Course
from model.data.education_data import EducationData
from model.data.event import Event
from model.logic.observable import Observable
from util.constants.views import ViewName


class Repository:
    # active app views
    active_view: Observable[ViewName] = Observable(ViewName.LOADING)

    # data lists
    courses: Observable[list[Course]] = Observable([])
    events: Observable[list[Event]] = Observable([])

    # selected event for single event view
    selected_event: Observable[Event] = Observable()

    # selected data for education data form view
    selected_education_data: Observable[Tuple[Union[Course, Event], Optional[EducationData], bool]] = Observable()

    # info whether app state has change (save handling)
    has_changed: Observable[bool] = Observable(False)

