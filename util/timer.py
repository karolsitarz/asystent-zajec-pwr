from threading import Timer

from model.repository import Repository


def run_timer():
    Repository.timer.value = Timer(3.0, run_timer)
    Repository.timer.value.start()
