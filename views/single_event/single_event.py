from tkinter import Frame, Tk, Canvas, Scrollbar, Label, Button

from model.data.event import Event
from util.constants.views import ViewName
from views.frame_view import FrameView
from views.single_event.single_event_viewmodel import SingleEventViewModel


class SingleEventView(FrameView):
    def __init__(self, root: Tk):
        super().__init__(root, ViewName.SINGLE_EVENT)
        self.view_model = SingleEventViewModel()

        self.canvas = Canvas(self)
        self.parent = Frame(self.canvas)

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.parent, anchor="nw")
        scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="right", fill="both", expand=True)

        self.setup_observers()
        self.setup_bindings()

    def setup_observers(self):
        def observe_event(event: Event):
            for child in self.parent.winfo_children():
                child.destroy()

            if event is None:
                return

            container = Frame(self.parent)
            Button(container, text="go back", command=self.view_model.go_back).pack()
            Label(container, text=event.course.code, anchor="w").pack(fill="x", expand=True)
            Label(container, text=event.course.name, anchor="w", font="Arial 12 bold").pack(fill="x", expand=True)
            Label(container, text=event.start.__str__(), anchor="w", font="Arial 11").pack(fill="x", expand=True)
            Label(container, text=event.course.lecturer, anchor="w").pack(fill="x", expand=True)
            Label(container, text=event.location, anchor="w").pack(fill="x", expand=True)
            container.pack(fill="both", expand=True, pady=10, padx=10)

        self.view_model.event.observe(observe_event)

    def setup_bindings(self):
        self.parent.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_frame, width=e.width)
        )
