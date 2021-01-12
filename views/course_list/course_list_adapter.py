from model.data.course import Course
from model.repository import Repository
from util.constants import ViewName


class CourseListAdapter:
    def __init__(self):
        self.courses = Repository.courses

    def toggle_course_visibility(self, course: Course):
        def action():
            course.toggle_hidden()
            self.courses.emit()
            Repository.has_changed.value = True

        return action

    @staticmethod
    def go_back():
        Repository.active_view.value = ViewName.EVENT_LIST
