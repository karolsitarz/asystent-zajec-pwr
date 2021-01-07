from model.data.course import Course
from model.data.event import Event
from model.logic.observable import Observable
from util.constants.views import ViewName


class Repository:
    active_view: Observable[ViewName] = Observable(ViewName.LOADING)
    courses: Observable[list[Course]] = Observable([])
    events: Observable[list[Event]] = Observable([])
    selected_event: Observable[Event] = Observable()
