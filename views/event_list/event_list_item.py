from tkinter import Frame, Label

from model.data.event import Event


class EventListItem(Frame):
    def __init__(self, parent, event: Event, is_before: bool, on_click, **kw):
        super().__init__(parent, **kw)
        color = "gray" if is_before else None

        Label(self, text=event.start.humanize(), anchor="w", fg=color).pack(fill="x", expand=True)
        label = Label(self, text=f"{event.course.type} {event.course.name}", anchor="w", font="Arial 10 bold", cursor="hand2", fg=color)
        label.pack(fill="x", expand=True)

        def on_enter(_):
            label["font"] = "Arial 10 bold underline"

        def on_leave(_):
            label["font"] = "Arial 10 bold"

        label.bind("<Button-1>", on_click)
        label.bind("<Enter>", on_enter)
        label.bind("<Leave>", on_leave)
