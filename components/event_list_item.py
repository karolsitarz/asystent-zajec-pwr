from tkinter import Frame, Label

from model.event import Event
from repository.view_repository import ViewRepository
from util.constants.views import LOADING


class EventListItem(Frame):
    def __init__(self, parent, event: Event, **kw):
        super().__init__(parent, **kw)

        Label(self, text=event.start.humanize(), anchor="w").pack(fill="x", expand=True)
        label = Label(self, text=event.course.name, anchor="w", font="Arial 10 bold", cursor="hand2")
        label.pack(fill="x", expand=True)

        def on_click(_):
            print(event)
            ViewRepository().active_view.value = LOADING

        def on_enter(_):
            label["font"] = "Arial 10 bold underline"

        def on_leave(_):
            label["font"] = "Arial 10 bold"

        label.bind("<Button-1>", on_click)
        label.bind("<Enter>", on_enter)
        label.bind("<Leave>", on_leave)
