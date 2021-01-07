from typing import Tuple

from model.logic.observable import Observable
from model.logic.response import Response
from model.repository import Repository
from util.constants.views import ViewName
from views.login.jsos_connect import jsos_login
from util.methods.local_data import save_data


class LoginViewModel:
    def __init__(self):
        super().__init__()
        self.__is_submitting = False
        self.status: Observable[Tuple[Response, str, str]] = Observable()

    def jsos_login(self, username: str, password: str):
        if self.__is_submitting:
            return

        self.status.value = (Response.loading, None, None)

        try:
            self.__is_submitting = True
            (courses, events) = jsos_login(username, password)
            Repository.events.value = events
            Repository.courses.value = courses
            save_data()
            self.status.value = (Response.success, "Dane pobrano pomyślnie", f"Pobrano {len(courses)} kursów i {len(events)} terminów")
            Repository.active_view.value = ViewName.EVENTS

        except Exception as e:
            self.status.value = (Response.error, "Wystąpił błąd", e)

        finally:
            self.__is_submitting = False
