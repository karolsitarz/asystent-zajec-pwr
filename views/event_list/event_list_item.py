from tkinter import Frame, Label

from model.data.event import Event


class EventListItem(Frame):
    def __init__(self, parent, event: Event, is_before: bool, on_click, **kw):
        super().__init__(parent, **kw)
        if is_before:
            fg = "gray"
            bg = "lightgray"
        else:
            fg = None
            bg = "white"

        Label(self, text=event.start.humanize(), anchor="w", fg=fg, bg=bg).pack(fill="x", expand=True)
        label = Label(self, text=f"{event.course.type} {event.course.name}", anchor="w", font="Arial 10 bold", cursor="hand2", fg=fg, bg=bg)
        label.pack(fill="x", expand=True)

        def on_enter(_):
            label["font"] = "Arial 10 bold underline"

        def on_leave(_):
            label["font"] = "Arial 10 bold"

        label.bind("<Button-1>", on_click)
        label.bind("<Enter>", on_enter)
        label.bind("<Leave>", on_leave)

        self["highlightbackground"] = "lightgray"
        self["highlightthickness"] = 1
        self["borderwidth"] = 5
        self["bg"] = bg
        self.pack(fill="x", expand=True, pady=5, padx=10)
