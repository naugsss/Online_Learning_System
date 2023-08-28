from src.controllers.courses import Courses
from src.controllers.student import Student
from src.helpers.validators import get_string_input
from src.models.database import get_from_db, update_db, delete_from_db
from src.utils import queries


class Admin(Courses):

    def calculate_earning(self):
        result = get_from_db(queries.COURSE_DETAILS)
        for row in result:
            name = get_from_db(queries.GET_NAME, (row[3],))
            print("****************************")
            print("Mentor name : ", name[0][0])
            print("Course name : ", row[2])
            print("Earnings : ", row[0] * row[1])

    def approve_course(self):
        result = get_from_db(queries.GET_COURSES_STATUS, ("pending", "active"))
        pending_course_count = 0
        if len(result) > 0:
            pending_course_count = result[0][0]
            print("pending_course_count")
            print(pending_course_count)
        if pending_course_count > 0:

            result = get_from_db(queries.PENDING_STATUS, ("pending",))
            keys = ["Name", "Duration", "Price"]

            print("Course details : \n")
            for row in result:
                values = [row[1], row[3], row[4]]
                result = dict(zip(keys, values))
                for key, value in result.items():
                    print(key + ": ", value)
                print("***************")

                admin_input = get_string_input("Do you want to approve or reject this course : ")
                if admin_input == "approve":
                    update_db(queries.UPDATE_PENDING_APPROVAL_STATUS, ("approved", row[0]))
                    print("**** Course approved successfully ****")
                else:
                    delete_from_db(queries.DELETE_FROM_MENTOR_COURSE, (row[0],))
                    delete_from_db(queries.DELETE_FROM_COURSES, (row[0],))
                    print("**** Course rejected ****")
            pending_course_count -= 1

    def delete_course(self):

        student = Student()
        content = student.list_course()
        user_input = get_string_input("Enter the name of the course you wish to delete : ")
        flag = 0
        for row in content:
            if row[1].lower() == user_input.lower():
                flag = 1
                update_db(queries.UPDATE_COURSE_STATUS, ("deactive", row[1]))
                print("**** Course marked as deactive successfully ****")
                break
        if flag == 0:
            print("No such course exists, please try again")

    def list_course(self):
        content = get_from_db(queries.GET_COURSES, ("approved",))

        keys = ["Name", "Duration", "Price", "Rating", "Status"]
        print("Courses available : \n")
        for row in content:
            values = [row[1], row[3], row[4], row[5], row[8]]
            result = dict(zip(keys, values))
            for key, value in result.items():
                print(key + ": ", value)
            print("***************")
