from application import Application
from model.repository import Repository
from util.constants import ViewName
from util.local_data import load_data


if __name__ == '__main__':
    root = Application()
    load_data()
    is_empty = not Repository.events.value or not Repository.courses.value
    Repository.active_view.value = ViewName.LOGIN if is_empty else ViewName.EVENT_LIST

    root.mainloop()
