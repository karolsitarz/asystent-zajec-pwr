from tkinter import messagebox, Label, TOP, Entry, Button, Toplevel, Frame, Tk
from model.repository import Repository
from util.jsos_connect import jsos_login


class LoginView(Toplevel):
    def __init__(self, owner: Tk):
        super().__init__(owner)
        self.title("Zaloguj do JSOS")
        self.minsize(200, 150)
        self.owner = owner
        self.is_submitting = False

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
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        if Repository.is_empty():
            self.owner.destroy()

    def send_jsos_login(self):
        if self.is_submitting:
            return

        try:
            self.is_submitting = True
            self.button["state"] = "disabled"
            self.update()
            (courses, events) = jsos_login(self.field_login.get(), self.field_password.get())
            Repository.set_courses(courses)
            Repository.set_events(events)
            messagebox.showinfo("Dane pobrano pomyślnie", f"Pobrano {len(courses)} kursów i {len(events)} terminów")
            self.destroy()
            self.owner.deiconify()
            self.is_submitting = False

        except Exception as e:
            self.button["state"] = "active"
            self.update()
            messagebox.showerror("Wystąpił błąd", e)
            self.is_submitting = False
