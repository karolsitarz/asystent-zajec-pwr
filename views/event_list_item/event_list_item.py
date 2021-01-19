from tkinter import Frame, Label

from model.data.event import Event
from views.event_list_item.event_list_item_adapter import EventListItemAdapter


class EventListItem(Frame):
    def __init__(self, parent, event: Event, is_before: bool, on_click, **kw):
        super().__init__(parent, **kw)
        self.__parent = parent
        self.adapter = EventListItemAdapter(event)
        fg, bg = ("gray", "lightgray") if is_before else (None, "white")

        self.__header = Label(self, text=self.adapter.time_string.value, anchor="w", fg=fg, bg=bg)
        self.__header.pack(fill="x", expand=True)
        self.__label = Label(self, text=f"{event.course.type} {event.course.name}", anchor="w", font="Arial 10 bold", cursor="hand2", fg=fg, bg=bg)
        self.__label.pack(fill="x", expand=True)

        self["highlightbackground"] = "lightgray"
        self["highlightthickness"] = 1
        self["borderwidth"] = 5
        self["bg"] = bg
        self.pack(fill="x", expand=True, pady=5, padx=10)

        self.setup_bindings(on_click)
        self.setup_observers()

    def setup_bindings(self, on_click):
        def on_enter(_):
            self.__label["font"] = "Arial 10 bold underline"

        def on_leave(_):
            self.__label["font"] = "Arial 10 bold"

        self.__label.bind("<Button-1>", on_click)
        self.__label.bind("<Enter>", on_enter)
        self.__label.bind("<Leave>", on_leave)

    def update_time(self, time):
        self.__header["text"] = time
        self.update()

    def setup_observers(self):
        self.adapter.time_string.observe(self.update_time)

    def destroy(self):
        self.adapter.time_string.unobserve(self.update_time)
        super().destroy()
