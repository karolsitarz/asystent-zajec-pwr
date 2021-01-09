import webbrowser
from tkinter import Frame, Label, Text, WORD, PhotoImage, Scrollbar

from model.data.education_data import EducationData
from util.constants import ASSETS
from util.image_button import ImageButton


class EducationDataItem(Frame):
    def __init__(self, parent, data: EducationData, on_button, **kw):
        super().__init__(parent, **kw)
        bg = "white"

        header = Frame(self, bg=bg)
        if data.is_url:
            self.__link_image = PhotoImage(file=ASSETS["link"])
            Label(header, image=self.__link_image, bg=bg).pack(side="left")
        label = Label(header, text=data.name, anchor="w", font="Arial 10 bold", bg=bg)
        label.pack(fill="x", expand=True, side="left")

        button_plus_event = ImageButton(header, tooltip="Edytuj notatkę", image=ASSETS["edit"], width=16, height=16)
        button_plus_event["command"] = on_button
        button_plus_event.pack(side="right")

        header.pack(fill="x")

        self.pack(fill="x", pady=2)
        self["highlightbackground"] = "lightgray"
        self["highlightthickness"] = 1
        self["borderwidth"] = 5
        self["bg"] = bg

        if not data.is_url:
            if len(data.value) > 0:
                text_container = Frame(self)
                scrollbar = Scrollbar(text_container)
                scrollbar.pack(side="right", fill="y")
                content = Text(text_container, height=5, wrap=WORD, border=0, yscrollcommand=scrollbar.set)
                scrollbar["command"] = content.yview
                content.insert('1.0', data.value)
                content.configure(state="disabled")
                content.pack(fill="x", expand=True, side="left")
                text_container.pack(fill="x", expand=True, padx=2)
                content.bind("<MouseWheel>", lambda _: "break")
        else:
            def on_enter(_):
                label["font"] = "Arial 10 bold underline"

            def on_leave(_):
                label["font"] = "Arial 10 bold"

            label["cursor"] = "hand2"
            label.bind("<Enter>", on_enter)
            label.bind("<Leave>", on_leave)
            label.bind("<Button-1>", lambda _: webbrowser.open(data.value))
