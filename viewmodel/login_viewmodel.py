from typing import Tuple

from repository.data_repository import DataRepository
from repository.view_repository import ViewRepository
from util.classes.observable import Observable
from util.classes.response import Response
from util.constants.views import LOADING
from util.methods.jsos_connect import jsos_login
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
            data_repository = DataRepository()
            data_repository.set_events(events)
            data_repository.set_courses(courses)
            save_data()
            self.status.value = (Response.success, "Dane pobrano pomyślnie", f"Pobrano {len(courses)} kursów i {len(events)} terminów")
            ViewRepository().active_view.value = LOADING

        except Exception as e:
            self.status.value = (Response.error, "Wystąpił błąd", e)

        finally:
            self.__is_submitting = False
