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
            keys = ["Name", "Duration", "Price", "Rating"]
            print("Courses available : \n")
            for row in content:
                values = [row[1], row[3], row[4], row[5]]
                result = dict(zip(keys, values))

                for key, value in result.items():
                    print(key + ": ", value)
                print("***************")

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
            print("********************")
            print("Name : ", user_name[0][0])
            print("Course purchased : ", course_name[0][0])
