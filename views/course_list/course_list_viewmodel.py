from model.data.course import Course
from model.repository import Repository
from util.constants.views import ViewName


class CourseListViewModel:
    def __init__(self):
        super().__init__()
        self.courses = Repository.courses

    def toggle_course_visibility(self, course: Course):
        def action():
            course.toggle_hidden()
            self.courses.emit()

        return action

    @staticmethod
    def go_back():
        Repository.active_view.value = ViewName.EVENT_LIST
