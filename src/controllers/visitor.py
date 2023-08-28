from src.controllers.courses import Courses
from src.models.database import get_from_db
from src.utils import queries


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
        keys = ["Name", "Duration", "Price", "Rating"]

        print("Courses available : \n")
        for row in content:
            values = [row[1], row[3], row[4], row[5]]

            result = dict(zip(keys, values))
            for key, value in result.items():
                print(key + ": ", value)
            print("***************")
        return content

