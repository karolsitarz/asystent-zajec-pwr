from http.cookiejar import CookieJar
from typing import Optional

import mechanize as mechanize
from bs4 import BeautifulSoup

from model.data.course import Course
from model.data.event import Event
from model.logic.datetime_epoch import DatetimeEpoch

ICAL_START = "DTSTART:"
ICAL_END = "DTEND:"
ICAL_LOCATION = "LOCATION:"
ICAL_SUMMARY = "SUMMARY:"
ICAL_END_VEVENT = "END:VEVENT"

LOGIN_URL = "https://jsos.pwr.edu.pl/index.php/site/loginAsStudent"
COURSES_URL = "https://jsos.pwr.edu.pl/index.php/student/zajecia"
ICAL_URL = "https://jsos.pwr.edu.pl/index.php/student/zajecia/iCalendar"


def jsos_login(username, password):
    cj = CookieJar()
    br = mechanize.Browser()
    br.set_cookiejar(cj)
    br.open(LOGIN_URL)

    br.select_form(nr=0)
    br.form["username"] = username
    br.form["password"] = password
    br.submit()

    if not br.geturl().endswith("/student/indeksDane"):
        soup = BeautifulSoup(br.response().read(), "html.parser")
        error_elem = soup.select_one(".message.error > span")
        if len(error_elem) == 0:
            raise Exception("Coś poszło nie tak. Spróbuj ponownie później.")

        raise Exception(error_elem.string)

    br.open(COURSES_URL)
    soup = BeautifulSoup(br.response().read(), "html.parser")
    elements = soup.select(".dane-content .listaTable tbody tr")
    if len(elements) == 0:
        raise Exception("Coś poszło nie tak. Spróbuj ponownie później.")

    courses: list[Course] = []
    for element in elements:
        data_el = element.select_one("td:nth-child(1)")
        split = list(data_el.stripped_strings)

        course_type = split[0][-1]
        name = split[1]
        lecturer = element.select_one("td:nth-child(2)").string
        code = element.select_one("td:nth-child(3)").string
        courses.append(Course(code, course_type, name, lecturer))

    br.open(ICAL_URL)
    decoded = br.response().read().decode("utf-8")
    lines: list[str] = decoded.splitlines()

    events: list[Event] = []
    start: Optional[DatetimeEpoch] = None
    end: Optional[DatetimeEpoch] = None
    location: Optional[str] = None
    course: Optional[Course] = None
    for line in lines:
        if line.startswith(ICAL_START):
            start = DatetimeEpoch.from_ical(line[len(ICAL_START):])
        elif line.startswith(ICAL_END):
            end = DatetimeEpoch.from_ical(line[len(ICAL_END):])
        elif line.startswith(ICAL_LOCATION):
            location = line[len(ICAL_LOCATION):]
        elif line.startswith(ICAL_SUMMARY):
            description = line[len(ICAL_SUMMARY):]
            course_type = description[0]
            name = description[2:]
            found_course = next((c for c in courses if Course.predicate(c, course_type, name)), None)
            if found_course is not None:
                course = found_course
        elif line == ICAL_END_VEVENT:
            if course is not None:
                events.append(Event(start, end, location, course))

            start = None
            end = None
            location = None
            course = None

    return courses, events
