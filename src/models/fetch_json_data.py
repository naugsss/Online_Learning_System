import json


class JsonData:
    data = None

    @classmethod
    def load_data(cls):
        if cls.data is None:
            with open(r'C:\\coding\WG\watchguard_daily_task_Aaryan\\online learning\\Online_Learning_System\src\\utils\\query_data.json','r') as file:
                cls.data = json.load(file)
        return cls.data
