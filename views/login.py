from tkinter import messagebox, Label, TOP, Entry, Button, Toplevel, Frame, Tk
from model.repository import Repository
from util.jsos_connect import jsos_login


class LoginView(Toplevel):
    def __init__(self, owner: Tk):
        super().__init__(owner)
        self.title("Zaloguj do JSOS")
        self.minsize(200, 150)

        # START create layout
        parent = Frame(self)
        Label(parent, text="Login").pack(side=TOP)
        self.field_login = Entry(parent)
        self.field_login.insert(0, "pwr308496")  # TODO: USED FOR DEBUGGING, DELETE LATER
        self.field_login.pack(side=TOP, pady=5)
        self.field_login.bind("<Return>", lambda event: self.send_jsos_login())

        Label(parent, text="Password").pack(side=TOP)
        self.field_password = Entry(parent, show="*")
        self.field_password.pack(side=TOP, pady=5)
        self.field_password.bind("<Return>", lambda event: self.send_jsos_login())

        self.button = Button(parent, text="Zaloguj", command=self.send_jsos_login)
        self.button.pack(side=TOP, pady=10)
        parent.pack(expand=1)
        # END create layout

        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: self.on_close(owner))

    def on_close(self, owner: Tk):
        if Repository.is_empty():
            owner.destroy()

    def send_jsos_login(self):
        try:
            self.button["state"] = "disabled"
            self.update()
            (courses, events) = jsos_login(self.field_login.get(), self.field_password.get())
            Repository.set_courses(courses)
            Repository.set_events(events)
            messagebox.showinfo("Dane pobrano pomyślnie", f"Pobrano {len(courses)} kursów i {len(events)} terminów")
            self.destroy()

        except Exception as e:
            self.button["state"] = "active"
            self.update()
            messagebox.showerror("Wystąpił błąd", e)
