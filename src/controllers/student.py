from tabulate import tabulate
from src.controllers.courses import Courses
from src.models.database import get_from_db
from src.utils import queries


class Student(Courses):

    def calculate_earning(self):
        pass

    def delete_course(self):
        pass

    def list_course(self):
        content = get_from_db(queries.GET_COURSES_STATUS, ("approved", "active"))
        if len(content) == 0:
            print("No course exists.")
        else:

            print("Courses available : \n")
            table = [(name, duration, price, rating) for (_, name, _, duration, price, rating, *_) in content]
            headers = ["Name", "Duration (in months)", "Price", "Rating"]
            table_str = tabulate(table, headers=headers, tablefmt="grid")
            print(table_str)

            return content

    def approve_course(self):
        pass

    @staticmethod
    def view_student_details():

        result = get_from_db(queries.GET_USER_DETAILS)
        print("Here are the details of the user:")

        for row in result:
            user_name = get_from_db(queries.GET_NAME, (row[1],))
            course_name = get_from_db(queries.GET_COURSE_NAME, (row[2],))
            table_data = [[user_name[0][0], course_name[0][0]]]
            print(tabulate(table_data, headers=['Name', 'Course Purchased'], tablefmt="grid"))

