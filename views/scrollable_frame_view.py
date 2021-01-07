from tkinter import Frame, Tk, Canvas, Scrollbar

from model.repository import Repository
from util.constants.views import ViewName
from views.frame_view import FrameView


class ScrollableFrameView(FrameView):
    def __init__(self, root: Tk, name: ViewName):
        self.container = Frame(root)
        self.__is_visible = False
        self.container.grid(row=0, column=0, sticky="news")

        self.canvas = Canvas(self.container)
        super().__init__(self.canvas, name)

        canvas_frame = self.canvas.create_window((0, 0), window=self, anchor="nw")
        scrollbar = Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="right", fill="both", expand=True)

        def observe(view: ViewName):
            if view == name:
                # when entering
                if not self.__is_visible:
                    self.canvas.bind_all(
                        "<MouseWheel>",
                        lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
                    )
                self.__is_visible = True
                self.container.tkraise()
            else:
                # when exiting
                if self.__is_visible:
                    self.canvas.unbind_all("<MouseWheel>")
                self.__is_visible = False

        Repository.active_view.observe(observe)

        self.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(canvas_frame, width=e.width)
        )
