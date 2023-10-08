import json


class JsonData:
    data = None

    @classmethod
    def load_data(cls):
        if cls.data is None:
            with open(r'C:\coding\WG\Online_Learning_System - Fast\src\utils\query_data.json','r') as file:
                cls.data = json.load(file)
        return cls.data
