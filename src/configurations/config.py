# import json


# class JsonData:
#     data = None

#     @classmethod
#     def load_data(cls):
#         if cls.data is None:
#             with open(
#                 r"C:\coding\WG\Online_Learning_System - Fast\src\utils\query_data.json",
#                 "r",
#             ) as file:
#                 cls.data = json.load(file)
#         return cls.data

import json

connection_parameters = None
error_format = None
access_control_list = None
sql_queries = None
prompts = None


def load_configuration():
    with open("src/configurations/config.json", "r") as fp:
        config = json.load(fp)
        prompts_path = config.get("prompts_path")
        sql_queries_path = config.get("sql_queries_path")
        access_control_list = config.get("access_control_list")
        prompts = get_prompts(prompts_path)
        QUERIES = get_sql_queries(sql_queries_path)

        return (
            connection_parameters,
            prompts,
            QUERIES,
            error_format,
            access_control_list,
        )


def get_prompts(prompts_path):
    with open(prompts_path, "r") as fp:
        return json.load(fp)


def get_sql_queries(sql_queries_path):
    with open(sql_queries_path, "r") as fp:
        return json.load(fp)


(
    connection_parameters,
    prompts,
    sql_queries,
    error_format,
    access_control_list,
) = load_configuration()
