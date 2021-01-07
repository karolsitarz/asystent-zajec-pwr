from tkinter import Tk, Button

from util.constants.views import ViewName
from views.event_list.event_list_item import EventListItem
from views.event_list.event_list_viewmodel import EventListViewModel
from views.scrollable_frame_view import ScrollableFrameView


class EventListView(ScrollableFrameView):
    def __init__(self, root: Tk):
        super().__init__(root, ViewName.EVENT_LIST)
        self.view_model = EventListViewModel()

        self.setup_observers()

    def setup_observers(self):
        def observe_events(data):
            for child in self.winfo_children():
                child.destroy()

            Button(self, text="toggle visibility", command=self.view_model.toggle_is_showing_all).pack()
            for (is_before, event) in data:
                on_click = self.view_model.on_event_selected(event)
                item = EventListItem(self, event, is_before, on_click)
                item.pack(fill="x", expand=True, pady=10, padx=10)

        self.view_model.events.observe(observe_events)
