from tkinter import messagebox, Label, TOP, Entry, Button, Frame, Tk

from util.classes.response import Response
from viewmodel.login_viewmodel import LoginViewModel


class LoginView(Frame):
    def __init__(self, root: Tk):
        super().__init__(root)
        self.__view_model = LoginViewModel()

        # START create layout
        parent = Frame(self)
        Label(parent, text="Login").pack(side=TOP)
        self.field_login = Entry(parent)
        self.field_login.insert(0, "pwr308496")  # TODO: USED FOR DEBUGGING, DELETE LATER
        self.field_login.pack(side=TOP, pady=2)
        self.field_login.bind("<Return>", lambda event: self.send_jsos_login())

        Label(parent, text="Password").pack(side=TOP)
        self.field_password = Entry(parent, show="*")
        self.field_password.pack(side=TOP, pady=2)
        self.field_password.bind("<Return>", lambda event: self.send_jsos_login())

        self.button = Button(parent, text="Zaloguj", command=self.send_jsos_login)
        self.button.pack(side=TOP, pady=10)
        parent.pack(expand=1)
        self.setup_observers()

    def setup_observers(self):
        def observe_status(data):
            (response, title, body) = data
            if response is Response.loading:
                self.button["state"] = "disabled"
                self.update()
                return

            if response is Response.error:
                messagebox.showerror(title, body)
            else:
                messagebox.showinfo(title, body)

            self.button["state"] = "active"
            self.update()

        self.__view_model.status.observe(observe_status)

    def send_jsos_login(self):
        self.__view_model.jsos_login(self.field_login.get(), self.field_password.get())
