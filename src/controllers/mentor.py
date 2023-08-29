from tabulate import tabulate

from src.controllers.courses import Courses
from src.helpers.validators import get_string_input
from src.models.database import insert_into_db, get_from_db
from src.utils import queries


class Mentor(Courses):
    def calculate_earning(self, user_id):

        message = "There was an error in displaying the earnings.."
        result = get_from_db(queries.GET_EARNING_DATA, (user_id,), message)
        for row in result:
            name = get_from_db(queries.GET_NAME, (user_id,), message)
            print("****************************")
            print("Mentor name : ", name[0][0])
            print("Course name : ", row[2])
            print("Earnings : ", row[0] * row[1])

    def delete_course(self):
        pass

    @staticmethod
    def add_mentor():
        user_name = get_string_input("Enter the username of the user whom you wish to make admin : ")
        message = "Couldn't add mentor, please try again ..."
        result = insert_into_db(queries.GET_FROM_AUTHENTICATION, (user_name,), message)
        insert_into_db(queries.INSERT_INTO_USER_ROLES, (result[0][3], 3), message)
        print("**** Mentor added successfully ****")

    def list_course(self):

        message = "There was error in listing the courses."
        content = get_from_db(queries.GET_COURSES, ("approved",), message)
        print("Courses available : \n")

        table = [(name, duration, price, rating, status) for (_, name, _, duration, price, rating, _, _, status, *_) in content]
        headers = ["Name", "Duration (in months)", "Price", "Rating", "Status"]
        table_str = tabulate(table, headers=headers, tablefmt="grid")
        print(table_str)
