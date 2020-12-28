from http.cookiejar import CookieJar
from tkinter import *
from tkinter import messagebox
import mechanize as mechanize
from bs4 import BeautifulSoup


def jsos_login(username, password):
    cj = CookieJar()
    br = mechanize.Browser()
    br.set_cookiejar(cj)
    br.open("https://jsos.pwr.edu.pl/index.php/site/loginAsStudent")

    br.select_form(nr=0)
    br.form["username"] = username
    br.form["password"] = password
    br.submit()

    if br.geturl().endswith("/student/indeksDane"):
        br.open("https://jsos.pwr.edu.pl/index.php/student/zajecia")
        soup = BeautifulSoup(br.response().read(), "html.parser")
        elements = soup.select('.dane-content .listaTable tbody tr')
        if len(elements) == 0:
            messagebox.showerror("Wystąpił błąd", "Coś poszło nie tak. Spróbuj ponownie później.")

        items = []
        for element in elements:
            data_el = element.select_one('td:nth-child(1)')
            split = list(data_el.stripped_strings)

            course_type = split[0][-1]
            name = split[1]
            lecturer = element.select_one('td:nth-child(2)').string
            code = element.select_one('td:nth-child(3)').string
            items.append({
                "course_type": course_type,
                "name": name,
                "lecturer": lecturer,
                "code": code,
            })

        print(items)

    else:
        soup = BeautifulSoup(br.response().read(), "html.parser")
        error_elem = soup.select_one('.message.error > span')
        if len(error_elem) == 0:
            messagebox.showerror("Wystąpił błąd", "Coś poszło nie tak. Spróbuj ponownie później.")

        messagebox.showerror("Wystąpił błąd", error_elem.string)


class LoginView(Toplevel):
    def __init__(self, owner):
        super().__init__(owner)
        self.title("Login to JSOS")
        self.minsize(250, 350)

        def create_layout():
            Label(self, text="Login").pack(side=TOP)
            self.field_login = Entry(self)
            self.field_login.insert(0, "pwr308496")  # TODO: USED FOR DEBUGGING, DELETE LATER
            self.field_login.pack(side=TOP)

            Label(self, text="Password").pack(side=TOP)
            self.field_password = Entry(self, show="*")
            self.field_password.pack(side=TOP)

            self.button = Button(self, text="Zaloguj")
            self.button.pack(side=TOP)
            self.button["command"] = lambda: jsos_login(self.field_login.get(), self.field_password.get())

            Label(self, text="Import an iCalendar file").pack(side=TOP)
            self.button_import = Button(self, text="Import")

        create_layout()
        self.grab_set()

        self.update()
        self.geometry("300x500")
