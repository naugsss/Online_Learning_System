import json

access_control_list = None
sql_queries = None


def load_configuration():
    with open("src/configurations/config.json", "r") as fp:
        config = json.load(fp)
        access_control_list = config.get("access_control_list")
        sql_queries = get_sql_queries()
        prompts = get_prompts()
        return (
            prompts,
            sql_queries,
            access_control_list,
        )


def get_sql_queries():
    with open(
        "src/utils/query_data.json",
        "r",
    ) as file:
        sql_queries = json.load(file)
        return sql_queries


def get_prompts():
    with open(
        "src/utils/prompts.json",
        "r",
    ) as file:
        prompts = json.load(file)
        return prompts


(
    prompts,
    sql_queries,
    access_control_list,
) = load_configuration()
