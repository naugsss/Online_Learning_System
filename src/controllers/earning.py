from tabulate import tabulate
from src.models.database import DatabaseConnection
from src.models.fetch_json_data import JsonData
# from src.utils import queries

DatabaseConnection = DatabaseConnection()
get_query = JsonData.load_data()

class Earning:
    def calculate_mentor_earning(self, user_id):
        result = DatabaseConnection.get_from_db(get_query["GET_EARNING_DATA"], (user_id,))
        values = []
        total_earning = 0
        for row in result:
            name = DatabaseConnection.get_from_db(get_query["GET_NAME"], (user_id,))
            values.append([name[0][0], row[2], row[0] * row[1]])
            total_earning += row[0] * row[1]
        print(tabulate(values, headers=["Name", "Course name", "Earning"], tablefmt="grid"))
        print("Your total earning is : Rs. ", total_earning)

    def calculate_all_mentor_earning(self):

        result = DatabaseConnection.get_from_db(get_query["COURSE_DETAILS"])
        if result is not None:
            values = []
            for row in result:
                name = DatabaseConnection.get_from_db(get_query["GET_NAME"], (row[3],))
                values.append([name[0][0], row[2], row[0] * row[1]])

            print(tabulate(values, headers=["Name", "Course name", "Earning"], tablefmt="grid"))
