from repository.data_repository import DataRepository


class EventsViewModel:
    def __init__(self):
        super().__init__()
        self.events = DataRepository().events
