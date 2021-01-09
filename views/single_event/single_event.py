from tkinter import Frame, Tk, Label

from model.data.event import Event
from util.constants import ViewName, ASSETS
from util.image_button import ImageButton
from views.scrollable_frame_view import ScrollableFrameView
from views.single_event.education_data_item import EducationDataItem
from views.single_event.single_event_viewmodel import SingleEventViewModel


class SingleEventView(ScrollableFrameView):
    def __init__(self, root: Tk):
        super().__init__(root, ViewName.SINGLE_EVENT)
        self.view_model = SingleEventViewModel()

        button_back = ImageButton(self.toolbar, tooltip="Powrót", image=ASSETS["back"])
        button_back["command"] = self.view_model.go_back
        button_back.pack(side="left", padx=2)

        self.setup_observers()

    def setup_observers(self):
        def observe_event(event: Event):
            for child in self.winfo_children():
                child.destroy()

            if event is None:
                return

            container = Frame(self)
            Label(container, text=event.course.code, anchor="w").pack(fill="x", expand=True)
            Label(container, text=event.course.name, anchor="w", font="Arial 12 bold").pack(fill="x", expand=True)
            Label(container, text=event.start.__str__(), anchor="w", font="Arial 11").pack(fill="x", expand=True)
            Label(container, text=event.course.lecturer, anchor="w").pack(fill="x", expand=True)
            Label(container, text=event.location, anchor="w").pack(fill="x", expand=True)
            container.pack(fill="both", expand=True, pady=10, padx=10)

            event_data_header = Frame(self)
            Label(event_data_header, text="Dane zajęć", anchor="w", font="Arial 11 bold").pack(side="left")

            button_plus_event = ImageButton(event_data_header, tooltip="Dodaj notatkę zajęć", image=ASSETS["plus"], width=16, height=16)
            button_plus_event["command"] = self.view_model.add_education_data(event, False)
            button_plus_event.pack(side="right", padx=5)

            event_data_header.pack(fill="both", expand=True, padx=10, pady=(20, 5))

            event_data = Frame(self)
            if len(event.data) == 0:
                Label(event_data, text="Zajęcia nie posiadają danych", font="Arial 9", fg="gray").pack(fill="x", expand=True, pady=5)

            for data in event.data:
                EducationDataItem(event_data, data, self.view_model.edit_education_data(event, data, False))
            event_data.pack(fill="both", expand=True, padx=10)

            course_data_header = Frame(self)
            Label(course_data_header, text="Dane kursu", anchor="w", font="Arial 11 bold").pack(side="left")

            button_plus_course = ImageButton(course_data_header, tooltip="Dodaj notatkę kursu", image=ASSETS["plus"], width=16, height=16)
            button_plus_course["command"] = self.view_model.add_education_data(event.course, is_course=True)
            button_plus_course.pack(side="right", padx=5)

            course_data_header.pack(fill="both", expand=True, padx=10, pady=(20, 5))

            course_data = Frame(self)
            if len(event.course.data) == 0:
                Label(course_data, text="Kurs nie posiada danych", font="Arial 9", fg="gray").pack(fill="x", expand=True, pady=5)

            for data in event.course.data:
                EducationDataItem(course_data, data, self.view_model.edit_education_data(event.course, data, is_course=True))
            course_data.pack(fill="both", expand=True, padx=10)

        self.view_model.event.observe(observe_event)
