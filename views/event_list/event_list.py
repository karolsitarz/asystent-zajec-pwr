from tkinter import Tk, Button, Label, messagebox

from util.constants import ViewName, ASSETS
from util.image_button import ImageButton
from util.local_data import save_data
from views.event_list.event_list_item import EventListItem
from views.event_list.event_list_viewmodel import EventListViewModel
from views.scrollable_frame_view import ScrollableFrameView


class EventListView(ScrollableFrameView):
    def __init__(self, root: Tk):
        super().__init__(root, ViewName.EVENT_LIST)
        self.view_model = EventListViewModel()

        self.button_visibility = ImageButton(self.toolbar, tooltip="Przełącz widoczność starych kursów", image=ASSETS["visible"])
        self.button_visibility["command"] = self.view_model.toggle_is_showing_all
        self.button_visibility.pack(side="left", padx=2)

        button_course_list = ImageButton(self.toolbar, tooltip="Lista kursów", image=ASSETS["list"])
        button_course_list["command"] = self.view_model.navigate_to_course_list
        button_course_list.pack(side="left", padx=2)

        button_clear_data = ImageButton(self.toolbar, tooltip="Wyczyść dane", image=ASSETS["trash"])
        button_clear_data["command"] = self.clear_data
        button_clear_data.pack(side="right", padx=2)

        self.button_save = ImageButton(self.toolbar, tooltip="Zapisz zmiany", image=ASSETS["save"], state="disabled")
        self.button_save["command"] = save_data
        self.button_save.pack(side="right", padx=2)

        self.setup_observers()

    def setup_observers(self):
        def observe_events(data):
            self.button_visibility.set_image(ASSETS["invisible"] if self.view_model.is_showing_all else ASSETS["visible"])

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
