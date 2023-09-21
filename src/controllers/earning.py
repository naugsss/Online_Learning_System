from tabulate import tabulate
from src.models.database import DatabaseConnection
from src.models.fetch_json_data import JsonData

DatabaseConnection = DatabaseConnection()
get_query = JsonData.load_data()


class Earning:
    def calculate_mentor_earning(self, user_id):
        result = DatabaseConnection.get_from_db(get_query.get("GET_EARNING_DATA"), (user_id,))
        values = []
        total_earning = 0
        if len(result) == 0 or result is None:
            return None
        for row in result:
            name = DatabaseConnection.get_from_db(get_query.get("GET_NAME"), (user_id,))
            values.append([name[0][0], row[2], row[0] * row[1]])
            total_earning += row[0] * row[1]
        print(tabulate(values, headers=["Name", "Course name", "Earning"], tablefmt="grid"))
        print("Your total earning is : Rs. ", total_earning)
        return values

    def calculate_all_mentor_earning(self):

        result = DatabaseConnection.get_from_db(get_query.get("COURSE_DETAILS"))
        if result is not None:
            values = []
            for row in result:
                name = DatabaseConnection.get_from_db(get_query.get("GET_NAME"), (row[3],))
                values.append([name[0][0], row[2], row[0] * row[1]])

            print(tabulate(values, headers=["Name", "Course name", "Earning"], tablefmt="grid"))
            return values
        return None