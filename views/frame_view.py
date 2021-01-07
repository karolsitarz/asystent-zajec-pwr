from tkinter import Frame, Tk

from model.repository import Repository
from util.constants.views import ViewName


class FrameView(Frame):
    def __init__(self, root, name: ViewName):
        super().__init__(root)
        self.grid(row=0, column=0, sticky="news")

        def observe(view: ViewName):
            if view == name:
                self.tkraise()

        Repository.active_view.observe(observe)
