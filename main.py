from tkinter import Tk, Frame

from repository.data_repository import DataRepository
from repository.view_repository import ViewRepository
from util.constants.views import LOGIN, LOADING, EVENTS
from util.methods.local_data import load_data
from view.events import EventsView
from view.loading import LoadingView
from view.login import LoginView


class Application(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Zdalne zajęcia PWR")
        self.minsize(250, 350)

        self.update()
        self.geometry("300x500")

        self.__views = {
            EVENTS: EventsView(self),
            LOGIN: LoginView(self),
            LOADING: LoadingView(self),
        }
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        view: Frame
        for view in self.__views.values():
            view.grid(row=0, column=0, sticky="news")

        self.setup_observers()

    def setup_observers(self):
        def observe_active_view(name: str):
            self.__views[name].tkraise()

        ViewRepository().active_view.observe(observe_active_view)


if __name__ == '__main__':
    root = Application()

    data_repository = DataRepository()
    load_data()
    ViewRepository().active_view.value = LOGIN if data_repository.is_empty() else EVENTS

    root.mainloop()
