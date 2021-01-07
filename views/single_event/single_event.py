from tkinter import Frame, Tk, Label, Button

from model.data.event import Event
from util.constants.views import ViewName
from views.scrollable_frame_view import ScrollableFrameView
from views.single_event.single_event_viewmodel import SingleEventViewModel


class SingleEventView(ScrollableFrameView):
    def __init__(self, root: Tk):
        super().__init__(root, ViewName.SINGLE_EVENT)
        self.view_model = SingleEventViewModel()

        self.setup_observers()

    def setup_observers(self):
        def observe_event(event: Event):
            for child in self.winfo_children():
                child.destroy()

            if event is None:
                return

            container = Frame(self)
            Button(container, text="go back", command=self.view_model.go_back).pack()
            Label(container, text=event.course.code, anchor="w").pack(fill="x", expand=True)
            Label(container, text=event.course.name, anchor="w", font="Arial 12 bold").pack(fill="x", expand=True)
            Label(container, text=event.start.__str__(), anchor="w", font="Arial 11").pack(fill="x", expand=True)
            Label(container, text=event.course.lecturer, anchor="w").pack(fill="x", expand=True)
            Label(container, text=event.location, anchor="w").pack(fill="x", expand=True)
            container.pack(fill="both", expand=True, pady=10, padx=10)

        self.view_model.event.observe(observe_event)
