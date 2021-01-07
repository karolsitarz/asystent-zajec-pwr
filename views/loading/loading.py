from tkinter import Label, Tk

from util.constants.views import ViewName
from views.frame_view import FrameView


class LoadingView(FrameView):
    def __init__(self, root: Tk):
        super().__init__(root, ViewName.LOADING)

        # START create layout
        Label(self, text="Loading...").pack(expand=1)
        # END create layout
