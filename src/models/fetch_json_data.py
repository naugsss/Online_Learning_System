import json


class JsonData:
    data = None

    @classmethod
    def load_data(cls):
        if cls.data is None:
            with open('C:\coding\WG\watchguard_daily_task_Aaryan\Online-Learning-System-Project - Copy with tests\src\\utils\query_data.json', 'r') as file:
                cls.data = json.load(file)
        return cls.data
