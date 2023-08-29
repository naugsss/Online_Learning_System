from src.controllers.courses import Courses
from src.models.database import get_from_db
from src.utils import queries
from tabulate import tabulate


class Visitor(Courses):

    def calculate_earning(self):
        pass

    def delete_course(self):
        pass

    def approve_course(self):
        pass

    def list_course(self):
        message = "There was some error in displaying course. Please try again."
        content = get_from_db(queries.GET_COURSES_STATUS, ("approved", "active"), message)

        table = [(name, duration, price, rating) for (_, name, _, duration, price, rating, *_) in content]
        headers = ["Name", "Duration (in months)", "Price", "Rating"]
        table_str = tabulate(table, headers=headers, tablefmt="grid")
        print(table_str)
        return content


