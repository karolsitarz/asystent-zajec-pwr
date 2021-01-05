from repository.data_repository import DataRepository
from util.classes.emitter import Emitter
from util.classes.response import Response
from util.methods.jsos_connect import jsos_login


class LoginViewModel(Emitter):
    def __init__(self):
        super().__init__()
        self.__is_submitting = False

    def jsos_login(self, username: str, password: str):
        if self.__is_submitting:
            return

        self.emit(Response.loading, None, None)

        try:
            self.__is_submitting = True
            (courses, events) = jsos_login(username, password)
            DataRepository().set_data(courses, events)
            self.emit(Response.success, "Dane pobrano pomyślnie", f"Pobrano {len(courses)} kursów i {len(events)} terminów")

        except Exception as e:
            self.emit(Response.error, "Wystąpił błąd", e)

        finally:
            self.__is_submitting = False
