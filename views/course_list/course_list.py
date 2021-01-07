from tkinter import Frame, Tk, Label, Button

from model.data.course import Course
from util.constants.views import ViewName
from views.course_list.course_list_viewmodel import CourseListViewModel
from views.scrollable_frame_view import ScrollableFrameView


class CourseListView(ScrollableFrameView):
    def __init__(self, root: Tk):
        super().__init__(root, ViewName.COURSE_LIST)
        self.view_model = CourseListViewModel()

        Button(self.toolbar, text="go back", command=self.view_model.go_back).pack(side="left")

        self.setup_observers()

    def setup_observers(self):
        def observe_event(courses: list[Course]):
            for child in self.winfo_children():
                child.destroy()

            for course in courses:

                item = Frame(self)
                Label(item, text=f"{course.type} {course.name}", anchor="w").pack(side="left")
                Button(item, text="hidden" if course.is_hidden else "visible", command=self.view_model.toggle_course_visibility(course)).pack(side="right")
                item.pack(fill="x", expand=True, pady=10, padx=10)

        self.view_model.courses.observe(observe_event)
