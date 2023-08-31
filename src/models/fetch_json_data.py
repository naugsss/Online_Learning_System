import json


class JsonData:
    data = None

    @classmethod
    def load_data(cls):
        if cls.data is None:
            with open('E:\projects\Online_Learning_System\src\\utils\data.json', 'r') as file:
                cls.data = json.load(file)
        return cls.data
