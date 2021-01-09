from tkinter import Frame, Label

from model.data.course import Course
from util.constants import ASSETS
from util.image_button import ImageButton


class CourseListItem(Frame):
    def __init__(self, root, course: Course, on_toggle):
        super().__init__(root)
        bg = "lightgray" if course.is_hidden else "white"
        fg = "gray" if course.is_hidden else None
        self["highlightbackground"] = "lightgray"
        self["highlightthickness"] = 1
        self["borderwidth"] = 5
        self["bg"] = bg

        Label(self, text=f"{course.type} {course.name}", anchor="w", bg=bg, fg=fg).pack(side="left")
        button = ImageButton(self, tooltip="Przełącz widoczność kursu w liście", image=ASSETS["invisible"] if course.is_hidden else ASSETS["visible"])
        button["command"] = on_toggle
        button.pack(side="right")
        self.pack(fill="x", expand=True, pady=5, padx=10)
