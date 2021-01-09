from tkinter import Tk, Button, Label, messagebox

from util.constants import ViewName
from util.local_data import save_data
from views.event_list.event_list_item import EventListItem
from views.event_list.event_list_viewmodel import EventListViewModel
from views.scrollable_frame_view import ScrollableFrameView


class EventListView(ScrollableFrameView):
    def __init__(self, root: Tk):
        super().__init__(root, ViewName.EVENT_LIST)
        self.view_model = EventListViewModel()

        Button(self.toolbar, text="toggle visibility", command=self.view_model.toggle_is_showing_all).pack(side="left")
        Button(self.toolbar, text="course list", command=self.view_model.navigate_to_course_list).pack(side="left")
        self.button_save = Button(self.toolbar, text="save data", command=save_data, state="disabled")
        self.button_save.pack(side="left")
        Button(self.toolbar, text="clear all data", command=self.clear_data).pack(side="right")

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

            self.canvas.update_idletasks()
            self.canvas.yview_moveto('0.0')

        self.view_model.events.observe(observe_events)

        def observe_changed(has_changed: bool):
            if has_changed:
                self.button_save["state"] = "normal"
            else:
                self.button_save["state"] = "disabled"

        self.view_model.has_changed.observe(observe_changed)

    def clear_data(self):
        if messagebox.askyesno("Uwaga!", "Ta operacja usunie wszystkie dane w aplikacji. Konieczne będzie ponowne zalogowanie. Czy na pewno chcesz kontynuować?"):
            self.view_model.clear_data()
