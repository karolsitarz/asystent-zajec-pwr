from tkinter import Tk

from model.repository import Repository
from util.constants.views import ViewName
from util.methods.local_data import load_data
from views.event_list.event_list import EventListView
from views.loading.loading import LoadingView
from views.login.login import LoginView
from views.single_event.single_event import SingleEventView


class Application(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Zdalne zajęcia PWR")
        self.minsize(250, 350)

        self.update()
        self.geometry("300x500")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # init views
        SingleEventView(self)
        EventListView(self)
        LoginView(self)
        LoadingView(self)


if __name__ == '__main__':
    root = Application()

    load_data()
    is_empty = len(Repository.events.value) == 0 or len(Repository.courses.value) == 0
    Repository.active_view.value = ViewName.LOGIN if is_empty else ViewName.EVENT_LIST

    root.mainloop()
