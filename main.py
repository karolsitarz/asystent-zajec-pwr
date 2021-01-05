from repository.data_repository import DataRepository
from repository.view_repository import ViewRepository
from util.constants.views import LOGIN, LOADING
from view.loading import *
from view.login import *


class Application(Tk, Observer):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Covid")
        self.minsize(250, 350)

        self.update()
        self.geometry("300x500")

        self.__views = {
            LOGIN: LoginView(self),
            LOADING: LoadingView(self),
        }
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        view: Frame
        for view in self.__views.values():
            view.grid(row=0, column=0, sticky="news")

        ViewRepository().add_observer(self)

    def observe(self, data):
        self.__views[data].tkraise()


if __name__ == '__main__':
    root = Application()
    DataRepository().load_data()
    root.mainloop()
