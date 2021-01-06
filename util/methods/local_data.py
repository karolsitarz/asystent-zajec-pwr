import json
import os

from model.course import Course
from model.event import Event
from repository.data_repository import DataRepository

DATA_PATH = "data.json"


def load_data():
    if not os.path.exists(DATA_PATH):
        return

    try:
        with open(DATA_PATH) as json_file:
            (parsed_courses, parsed_events) = json.load(json_file)
            courses = [Course.from_dict(data) for data in parsed_courses]
            events = [Event.from_dict(data, courses) for data in parsed_events]

            data_repository = DataRepository()
            data_repository.courses.value = courses
            data_repository.events.value = events

    except Exception as e:
        print(e)


def save_data():
    data_repository = DataRepository()
    parsed_courses = [c.to_dict() for c in data_repository.courses.value]
    parsed_events = [e.to_dict() for e in data_repository.events.value]
    with open(DATA_PATH, "w") as out:
        json.dump((parsed_courses, parsed_events), out)
