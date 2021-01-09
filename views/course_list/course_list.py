from tkinter import Tk

from model.data.course import Course
from util.constants import ViewName, ASSETS
from util.image_button import ImageButton
from views.course_list.course_list_item import CourseListItem
from views.course_list.course_list_viewmodel import CourseListViewModel
from views.scrollable_frame_view import ScrollableFrameView


class CourseListView(ScrollableFrameView):
    def __init__(self, root: Tk):
        super().__init__(root, ViewName.COURSE_LIST)
        self.view_model = CourseListViewModel()

        button_back = ImageButton(self.toolbar, tooltip="Powrót", image=ASSETS["back"])
        button_back["command"] = self.view_model.go_back
        button_back.pack(side="left", padx=2)

        self.setup_observers()

    def setup_observers(self):
        def observe_event(courses: list[Course]):
            (top, _) = self.canvas.yview()
            for child in self.winfo_children():
                child.destroy()

            for course in courses:
                CourseListItem(self, course, self.view_model.toggle_course_visibility(course))

            self.canvas.update_idletasks()
            self.canvas.yview_moveto(top)

        self.view_model.courses.observe(observe_event)
