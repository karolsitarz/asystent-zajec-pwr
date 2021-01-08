import webbrowser
from tkinter import Frame, Label

from model.data.education_data import EducationData


class EducationDataItem(Frame):
    def __init__(self, parent, data: EducationData, **kw):
        super().__init__(parent, **kw)

        label = Label(self, text=data.name, anchor="w", font="Arial 10 bold", cursor="hand2")
        label.pack(fill="x", expand=True)

        if not data.is_url:
            Label(self, text=data.value, anchor="w").pack(fill="x", expand=True)
        else:
            def on_enter(_):
                label["font"] = "Arial 10 bold underline"

            def on_leave(_):
                label["font"] = "Arial 10 bold"

            label.bind("<Enter>", on_enter)
            label.bind("<Leave>", on_leave)
            label.bind("<Button-1>", lambda _: webbrowser.open(data.value))
