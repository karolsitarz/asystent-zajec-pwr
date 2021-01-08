from tkinter import Tk, messagebox

from model.repository import Repository
from util.constants.views import ViewName
from util.methods.local_data import load_data, save_data
from views.course_list.course_list import CourseListView
from views.education_data_form.education_data_form import EducationDataFormView
from views.event_list.event_list import EventListView
from views.loading.loading import LoadingView
from views.login.login import LoginView
from views.single_event.single_event import SingleEventView

TITLE = "Zdalne zajęcia PWR"


class Application(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title(TITLE)
        self.minsize(250, 350)

        self.update()
        self.geometry("300x500")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # init views
        EducationDataFormView(self)
        SingleEventView(self)
        EventListView(self)
        LoginView(self)
        CourseListView(self)
        LoadingView(self)

        self.setup_observers()
        self.setup_handlers()

    def setup_observers(self):
        def observe_has_changed(has_changed: bool):
            if has_changed:
                self.title(f"*{TITLE}")
            else:
                self.title(TITLE)

        Repository.has_changed.observe(observe_has_changed)

    def setup_handlers(self):
        def on_close():
            if Repository.has_changed.value:
                response = messagebox.askyesnocancel("Uwaga!", "Masz niezapisane zmiany! Czy chcesz je zapisać?")
                if response is None:
                    return
                if response is True:
                    save_data()

            self.destroy()

        self.protocol("WM_DELETE_WINDOW", on_close)


if __name__ == '__main__':
    root = Application()

    load_data()
    is_empty = len(Repository.events.value) == 0 or len(Repository.courses.value) == 0
    Repository.active_view.value = ViewName.LOGIN if is_empty else ViewName.EVENT_LIST

    root.mainloop()
