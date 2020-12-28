from tkinter import *
from tkinter import messagebox, filedialog
import os
from includes.webbot.webbot import Browser

CHROME_PATHS = [
    r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"D:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"D:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]


def jsos_login(parent, login, password):
    paths = list(filter(lambda p: os.path.isfile(p), CHROME_PATHS))

    def action_login(binary_location=None):
        web = Browser(binary_location=binary_location)
        web.go_to("https://jsos.pwr.edu.pl/index.php/site/loginAsStudent")
        web.type(login, css_selector="#username")
        web.type(password, css_selector="#password")
        web.click(css_selector="#id2")
        if web.get_current_url().startswith("https://jsos.pwr.edu.pl/index.php/student/indeksDane"):
            web.go_to("https://jsos.pwr.edu.pl/index.php/student/zajecia")
            elements = web.find_elements(css_selector=".dane-content .listaTable tbody tr")
            print(web.get_page_source())
        else:
            errors = web.find_elements(css_selector=".message.error", number=1)
            if len(errors) > 0:
                messagebox.showerror("An error has occured", errors[0].text)

        web.close_current_tab()

    for i in range(len(paths)):
        try:
            action_login(paths[i])
            return

        except Exception as e:
            print(e)

    response = messagebox.askokcancel("Chrome not found!",
                                      "chrome.exe was not found in the default location. Do you want to select \"chrome.exe\" by yourself?")
    if response:
        path = select_chrome(parent)
        if path is not None:
            try:
                action_login(path)

            except Exception as e:
                messagebox.showerror("An error has occured", "Chrome wasn't found.")
                print(e)


def select_chrome(parent):
    return filedialog.askopenfilename(parent=parent, title="Open Chrome executable...", filetypes=[("Chrome executable", "chrome.exe")])


class LoginView(Toplevel):
    def __init__(self, owner):
        super().__init__(owner)
        self.title("Login to JSOS")
        self.minsize(250, 350)

        def create_layout():
            Label(self, text="Login").pack(side=TOP)
            self.field_login = Entry(self)
            self.field_login.pack(side=TOP)

            Label(self, text="Password").pack(side=TOP)
            self.field_password = Entry(self, show="*")
            self.field_password.pack(side=TOP)

            self.button = Button(self, text="Zaloguj")
            self.button.pack(side=TOP)
            self.button["command"] = lambda: jsos_login(self, self.field_login.get(), self.field_password.get())

            Label(self, text="Import an iCalendar file").pack(side=TOP)
            self.button_import = Button(self, text="Import")

        create_layout()
        self.grab_set()

        self.update()
        self.geometry("300x500")
