class EducationData:
    def __init__(self, name: str, value: str, is_url: bool):
        self.__name = name
        self.__value = value
        self.__is_url = is_url

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @property
    def is_url(self):
        return self.__is_url

    def to_dict(self):
        return {
            "name": self.__name,
            "value": self.__value,
            "is_url": self.__is_url,
        }

    @classmethod
    def from_dict(cls, data):
        return EducationData(data["name"], data["value"], data["is_url"])

    def update(self, name, value, is_url):
        self.__name = name
        self.__value = value
        self.__is_url = is_url


class EducationDataContainer:
    def __init__(self):
        self.__data: list[EducationData] = []

    @property
    def data(self):
        return self.__data

    def add_data(self, item: EducationData):
        self.__data.append(item)

    def delete_data(self, item: EducationData):
        self.__data.remove(item)

    def list_to_json(self):
        return [data.to_dict() for data in self.__data]

    def list_from_json(self, data):
        self.__data = [EducationData.from_dict(item) for item in data]
