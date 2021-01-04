from tkinter import Tk

from views.login import *


class Application(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Covid")
        self.minsize(250, 350)

        self.update()
        self.geometry("300x500")

        if Repository.is_empty():
            self.withdraw()
            LoginView(self)

        # self.create_menu()
        # self.create_toolbar()
        # self.create_location_options()
        # self.create_length_field()
        # self.create_type_options()
        # self.create_month_options()
        # self.create_day_options()
        # self.create_button()
        # self.create_list()
        # self.create_statusbar()


if __name__ == '__main__':
    root = Application()
    root.mainloop()
