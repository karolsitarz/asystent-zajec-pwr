from tkinter import Button, PhotoImage

from includes.ToolTip import ToolTip


class ImageButton(Button):
    def __init__(self, parent, image: str, tooltip: str = "", width=25, height=25, **kw):
        self.__image = PhotoImage(file=image)
        super().__init__(parent, **kw, width=width, height=height, border=1, highlightbackground="red")
        self["image"] = self.__image
        ToolTip(self, text=tooltip)

    def set_image(self, image):
        self.__image = PhotoImage(file=image)
        self["image"] = self.__image
