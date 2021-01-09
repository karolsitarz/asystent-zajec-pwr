from tkinter import messagebox, Label, Entry, Button, Frame, Tk

from model.logic.response import Response
from util.constants import ViewName
from views.frame_view import FrameView
from views.login.login_viewmodel import LoginViewModel


class LoginView(FrameView):
    def __init__(self, root: Tk):
        super().__init__(root, ViewName.LOGIN)
        self.view_model = LoginViewModel()

        # START create layout
        parent = Frame(self)
        Label(parent, text="Nazwa użytkownika").pack()
        self.field_login = Entry(parent)
        self.field_login.insert(0, "pwr308496")  # TODO: USED FOR DEBUGGING, DELETE LATER
        self.field_login.pack(pady=(5, 10))
        self.field_login.bind("<Return>", self.send_jsos_login)

        Label(parent, text="Hasło").pack()
        self.field_password = Entry(parent, show="*")
        self.field_password.pack(pady=(5, 10))
        self.field_password.bind("<Return>", self.send_jsos_login)

        self.button = Button(parent, text="Zaloguj", command=self.send_jsos_login, padx=10)
        self.button.pack(pady=10)

        self.info = Label(parent, justify="center", wraplength=300)
        self.info.pack()

        parent.pack(expand=1)
        self.setup_observers()

    def setup_observers(self):
        def observe_status(data):
            (response, content) = data
            if response is Response.loading:
                self.info["fg"] = "gray"
                self.info["text"] = content
                self.button["state"] = "disabled"
                self.update()
                return

            self.button["state"] = "active"

            if response is Response.success:
                messagebox.showinfo("Dane załadowano pomyślnie", content)
                self.info["text"] = ""
                return

            self.info["fg"] = "red"
            self.info["text"] = content
            self.update()

        self.view_model.status.observe(observe_status)

    def send_jsos_login(self, _=None):
        self.info["text"] = ""
        self.view_model.jsos_login(self.field_login.get(), self.field_password.get())
