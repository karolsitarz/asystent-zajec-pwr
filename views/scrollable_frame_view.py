from tkinter import Frame, Tk, Canvas, Scrollbar

from model.repository import Repository
from util.constants.views import ViewName
from views.frame_view import FrameView


class ScrollableFrameView(FrameView):
    def __init__(self, root: Tk, name: ViewName):
        self.container = Frame(root)
        self.container.grid(row=0, column=0, sticky="news")

        self.toolbar = Frame(self.container)
        self.toolbar.pack(fill="x")

        self.canvas = Canvas(self.container)
        super().__init__(self.canvas, name)

        def yview(*args):
            if self.canvas.yview() == (0.0, 1.0):
                return
            self.canvas.yview(*args)

        canvas_frame = self.canvas.create_window((0, 0), window=self, anchor="nw")
        scrollbar = Scrollbar(self.container, orient="vertical", command=yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="right", fill="both", expand=True)

        def observe(view: ViewName):
            if view == name:
                root.bind_all("<MouseWheel>", lambda e: yview("scroll", int(-1 * (e.delta / 120)), "units"))
                self.container.tkraise()

        Repository.active_view.observe(observe)

        self.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(canvas_frame, width=e.width)
        )
