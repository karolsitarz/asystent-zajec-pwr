from enum import Enum, auto


class ViewName(Enum):
    LOADING = auto()
    LOGIN = auto()
    EVENT_LIST = auto()
    SINGLE_EVENT = auto()
    COURSE_LIST = auto()
    EDUCATION_DATA_FORM = auto()


url_pattern = r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"


ASSETS = {
    "icon": "assets/icon.ico",
    "visible": "assets/visible.png",
    "invisible": "assets/invisible.png",
    "save": "assets/save.png",
    "logout": "assets/logout.png",
    "plus": "assets/plus.png",
    "back": "assets/back.png",
    "edit": "assets/edit.png",
    "list": "assets/list.png",
    "link": "assets/link.png",
}
