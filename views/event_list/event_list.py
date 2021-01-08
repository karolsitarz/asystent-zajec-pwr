from tkinter import Tk, Button, Label

from util.constants.views import ViewName
from util.methods.local_data import save_data
from views.event_list.event_list_item import EventListItem
from views.event_list.event_list_viewmodel import EventListViewModel
from views.scrollable_frame_view import ScrollableFrameView


class EventListView(ScrollableFrameView):
    def __init__(self, root: Tk):
        super().__init__(root, ViewName.EVENT_LIST)
        self.view_model = EventListViewModel()

        Button(self.toolbar, text="toggle visibility", command=self.view_model.toggle_is_showing_all).pack(side="left")
        Button(self.toolbar, text="course list", command=self.view_model.navigate_to_course_list).pack(side="left")
        Button(self.toolbar, text="save data", command=save_data).pack(side="left")

        self.setup_observers()

    def setup_observers(self):
        def observe_events(data):
            for child in self.winfo_children():
                child.destroy()

            if len(data) == 0:
                Label(self, text="Brak dostępnych zajęć").pack(fill="y", expand=True, pady=10, padx=10)

            for (is_before, event) in data:
                on_click = self.view_model.on_event_selected(event)
                EventListItem(self, event, is_before, on_click)

        self.view_model.events.observe(observe_events)
