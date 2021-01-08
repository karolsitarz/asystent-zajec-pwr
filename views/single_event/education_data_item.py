import webbrowser
from tkinter import Frame, Label, Text, WORD, Button

from model.data.education_data import EducationData


class EducationDataItem(Frame):
    def __init__(self, parent, data: EducationData, on_button, **kw):
        super().__init__(parent, **kw)
        bg = "white"
        fg = "blue" if data.is_url else None

        header = Frame(self, bg=bg)
        label = Label(header, text=data.name, anchor="w", font="Arial 10 bold", bg=bg, fg=fg)
        label.pack(fill="x", expand=True, side="left")
        Button(header, text="e", command=on_button).pack(side="right")
        header.pack(fill="x")

        self.pack(fill="x", pady=2)
        self["highlightbackground"] = "lightgray"
        self["highlightthickness"] = 1
        self["borderwidth"] = 5
        self["bg"] = bg

        if not data.is_url:
            if len(data.value) > 0:
                content = Text(self, height=5, wrap=WORD, border=0)
                content.insert('1.0', data.value)
                content.configure(state="disabled")
                content.pack(fill="x", expand=True, padx=2, side="top")
        else:
            def on_enter(_):
                label["font"] = "Arial 10 bold underline"

            def on_leave(_):
                label["font"] = "Arial 10 bold"

            label["cursor"] = "hand2"
            label.bind("<Enter>", on_enter)
            label.bind("<Leave>", on_leave)
            label.bind("<Button-1>", lambda _: webbrowser.open(data.value))
