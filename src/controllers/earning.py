from tabulate import tabulate
from src.models.database import DatabaseConnection
from src.utils import queries

DatabaseConnection = DatabaseConnection()


class Earning:
    def calculate_mentor_earning(self, user_id):
        result = DatabaseConnection.get_from_db(queries.GET_EARNING_DATA, (user_id,))
        values = []
        total_earning = 0
        if len(result) == 0 or result is None:
            print("You haven't made any course till now.")
            return
        for row in result:
            name = DatabaseConnection.get_from_db(queries.GET_NAME, (user_id,))
            values.append([name[0][0], row[2], row[0] * row[1]])
            total_earning += row[0] * row[1]
        print(tabulate(values, headers=["Name", "Course name", "Earning"], tablefmt="grid"))
        print("Your total earning is : Rs. ", total_earning)

    def calculate_all_mentor_earning(self):

        result = DatabaseConnection.get_from_db(queries.COURSE_DETAILS)
        if result is not None:
            values = []
            for row in result:
                name = DatabaseConnection.get_from_db(queries.GET_NAME, (row[3],))
                values.append([name[0][0], row[2], row[0] * row[1]])

            print(tabulate(values, headers=["Name", "Course name", "Earning"], tablefmt="grid"))
