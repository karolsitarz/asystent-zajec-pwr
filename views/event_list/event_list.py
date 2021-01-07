from tkinter import Frame, Tk, Canvas, Scrollbar, Button

from views.event_list.event_list_item import EventListItem
from util.constants.views import ViewName
from views.event_list.event_list_viewmodel import EventListViewModel
from views.frame_view import FrameView


class EventListView(FrameView):
    def __init__(self, root: Tk):
        super().__init__(root, ViewName.EVENT_LIST)
        self.view_model = EventListViewModel()
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
        def observe_events(data):
            for child in self.parent.winfo_children():
                child.destroy()

            Button(self.parent, text="toggle visibility", command=self.view_model.toggle_is_showing_all).pack()
            for (is_before, event) in data:
                on_click = self.view_model.on_event_selected(event)
                item = EventListItem(self.parent, event, is_before, on_click)
                item.pack(fill="x", expand=True, pady=10, padx=5)

        self.view_model.events.observe(observe_events)

    def setup_bindings(self):
        self.parent.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_frame, width=e.width)
        )
        self.canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        )
