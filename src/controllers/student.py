from tabulate import tabulate
from src.controllers.courses import Courses
from src.models.database import DatabaseConnection
from src.utils import queries

DatabaseConnection = DatabaseConnection()


class Student(Courses):


    def list_course(self):
        content = DatabaseConnection.get_from_db(queries.GET_COURSES_STATUS, ("approved", "active"))
        if len(content) == 0:
            print("No course exists.")
        else:

            print("Courses available : \n")
            table = [(name, duration, price, rating) for (_, name, _, duration, price, rating, *_) in content]
            headers = ["Name", "Duration (in months)", "Price", "Rating"]
            table_str = tabulate(table, headers=headers, tablefmt="grid")
            print(table_str)

            return content

    def view_student_details(self):

        result = DatabaseConnection.get_from_db(queries.GET_USER_DETAILS)
        print("Here are the details of the user:")
        values = []
        for row in result:
            user_name = DatabaseConnection.get_from_db(queries.GET_NAME, (row[1],))
            course_name = DatabaseConnection.get_from_db(queries.GET_COURSE_NAME, (row[2],))
            values.append([user_name[0][0], course_name[0][0]])

        print(tabulate(values, headers=['Name', 'Course Purchased'], tablefmt="grid"))

