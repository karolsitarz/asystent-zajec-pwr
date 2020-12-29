from http.cookiejar import CookieJar
from tkinter import messagebox, Label, TOP, Entry, Button, Toplevel
import mechanize as mechanize
from bs4 import BeautifulSoup

from model.repository import Event, Course, Repository

ICAL_START = "DTSTART:"
ICAL_END = "DTEND:"
ICAL_LOCATION = "LOCATION:"
ICAL_SUMMARY = "SUMMARY:"
ICAL_END_VEVENT = "END:VEVENT"


def jsos_login(username, password):
    cj = CookieJar()
    br = mechanize.Browser()
    br.set_cookiejar(cj)
    br.open("https://jsos.pwr.edu.pl/index.php/site/loginAsStudent")

    br.select_form(nr=0)
    br.form["username"] = username
    br.form["password"] = password
    br.submit()

    if not br.geturl().endswith("/student/indeksDane"):
        soup = BeautifulSoup(br.response().read(), "html.parser")
        error_elem = soup.select_one(".message.error > span")
        if len(error_elem) == 0:
            messagebox.showerror("Wystąpił błąd", "Coś poszło nie tak. Spróbuj ponownie później.")
            return

        messagebox.showerror("Wystąpił błąd", error_elem.string)
        return

    br.open("https://jsos.pwr.edu.pl/index.php/student/zajecia")
    soup = BeautifulSoup(br.response().read(), "html.parser")
    elements = soup.select(".dane-content .listaTable tbody tr")
    if len(elements) == 0:
        messagebox.showerror("Wystąpił błąd", "Coś poszło nie tak. Spróbuj ponownie później.")
        return

    courses: list[Course] = []
    for element in elements:
        data_el = element.select_one("td:nth-child(1)")
        split = list(data_el.stripped_strings)

        course_type = split[0][-1]
        name = split[1]
        lecturer = element.select_one("td:nth-child(2)").string
        code = element.select_one("td:nth-child(3)").string
        courses.append(Course(code, course_type, name, lecturer))

    br.open("https://jsos.pwr.edu.pl/index.php/student/zajecia/iCalendar")
    decoded = br.response().read().decode("utf-8")
    lines: list[str] = decoded.splitlines()

    events: list[Event] = []
    start = None
    end = None
    location = None
    code = None
    for line in lines:
        if line.startswith(ICAL_START):
            start = line[len(ICAL_START):]
        elif line.startswith(ICAL_END):
            end = line[len(ICAL_END):]
        elif line.startswith(ICAL_LOCATION):
            location = line[len(ICAL_LOCATION):]
        elif line.startswith(ICAL_SUMMARY):
            description = line[len(ICAL_SUMMARY):]
            course_type = description[0]
            name = description[2:]
            course = next((c for c in courses if Course.predicate(c, course_type, name)), None)
            if course is not None:
                code = course.code
        elif line == ICAL_END_VEVENT:
            if code is not None:
                events.append(Event(start, end, location, code))

            start = None
            end = None
            location = None
            code = None

    Repository.set_courses(courses)
    Repository.set_events(events)


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
