import traceback
from typing import Tuple

from model.logic.observable import Observable
from model.logic.response import Response
from model.repository import Repository
from util.constants import ViewName
from util.timer import run_timer
from views.login.jsos_connect import jsos_login, LoginException


class LoginAdapter:
    def __init__(self):
        self.__is_submitting = False
        self.status: Observable[Tuple[Response, str, str]] = Observable()

    def jsos_login(self, username: str, password: str):
        if self.__is_submitting:
            return

        try:
            self.__is_submitting = True
            (courses, events) = jsos_login(self.status, username, password)
            Repository.events.value = events
            Repository.courses.value = courses
            Repository.has_changed.value = True
            Repository.active_view.value = ViewName.EVENT_LIST
            run_timer()

        except LoginException:
            pass

        except Exception as e:
            print(e)
            self.status.value = (Response.error, "Wystąpił błąd. Spróbuj ponownie później.")
            traceback.print_exc()

        finally:
            self.__is_submitting = False
