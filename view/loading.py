from tkinter import Label, Frame, Tk


class LoadingView(Frame):
    def __init__(self, root: Tk):
        super().__init__(root)

        # START create layout
        Label(self, text="Loading...").pack(expand=1)
        # END create layout
