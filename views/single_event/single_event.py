from tkinter import Frame, Tk, Canvas, Scrollbar, Label

from model.data.event import Event
from util.constants.views import ViewName
from views.frame_view import FrameView


class SingleEventView(FrameView):
    def __init__(self, root: Tk):
        super().__init__(root, ViewName.SINGLE_EVENT)

        self.canvas = Canvas(self)
        self.parent = Frame(self.canvas)

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.parent, anchor="nw")
        scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="right", fill="both", expand=True)

        self.setup_bindings()

    def setup_bindings(self):
        self.parent.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_frame, width=e.width)
        )
        # self.canvas.bind_all(
        #     "<MouseWheel>",
        #     lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        # )

    def setup_data(self):

        Label(self, text=":D", anchor="w").pack(fill="x", expand=True)
