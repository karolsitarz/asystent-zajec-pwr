from tkinter import Frame, Label, Button

from model.data.course import Course


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
        Button(self, text="hidden" if course.is_hidden else "visible", command=on_toggle).pack(side="right")
        self.pack(fill="x", expand=True, pady=5, padx=10)
