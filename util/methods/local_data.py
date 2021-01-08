import json
import os
import traceback

from model.data.course import Course
from model.data.event import Event
from model.repository import Repository

DATA_PATH = "data.json"


def load_data():
    if not os.path.exists(DATA_PATH):
        return

    try:
        with open(DATA_PATH) as json_file:
            (parsed_courses, parsed_events) = json.load(json_file)
            courses = [Course.from_dict(data) for data in parsed_courses]
            events = [Event.from_dict(data, courses) for data in parsed_events]

            Repository.courses.value = courses
            Repository.events.value = events

    except Exception as e:
        print(e)
        traceback.print_exc()


def save_data():
    parsed_courses = [c.to_dict() for c in Repository.courses.value]
    parsed_events = [e.to_dict() for e in Repository.events.value]
    with open(DATA_PATH, "w") as out:
        json.dump((parsed_courses, parsed_events), out)
