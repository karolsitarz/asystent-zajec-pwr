from tkinter import Frame, Tk, Canvas, Scrollbar

from components.event_list_item import EventListItem
from viewmodel.events_viewmodel import EventsViewModel


class EventsView(Frame):
    def __init__(self, root: Tk):
        super().__init__(root)
        self.view_model = EventsViewModel()
        self.canvas = Canvas(self)
        scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.parent = Frame(self.canvas)
        canvas_frame = self.canvas.create_window((0, 0), window=self.parent, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="right", fill="both", expand=True)
        self.view_model.events.observe(self.observe_events)
        self.parent.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind(
            "<Configure>", lambda e: self.canvas.itemconfig(canvas_frame, width=e.width)
        )
        self.canvas.bind_all('<MouseWheel>',
                             lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

    def observe_events(self, events_list):
        for child in self.parent.winfo_children():
            child.destroy()

        for event in events_list:
            EventListItem(self.parent, event).pack(fill="x", expand=True, pady=10, padx=5)
