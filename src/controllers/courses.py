from abc import abstractmethod, ABC
from src.helpers.validators import get_string_input, get_int_input
from datetime import date
from src.models.context_manager import DatabaseConnection
from src.models.database import get_from_db, insert_into_db, update_db
from src.utils import queries


class Courses(ABC):

    def __init__(self):
        pass

    def add_course(self, user_id):
        course_name = get_string_input("Enter name of course : ")
        content = get_string_input("Enter content of course : ")
        duration = get_int_input("Enter duration of course in months : ")
        price = get_int_input("Enter price of course : ")

        try:
            with DatabaseConnection() as db:
                cursor = db.cursor()
                sql = "INSERT INTO courses (name, content, duration, price, avg_rating, approval_status, no_of_students, status, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (course_name, content, duration, price, 0, "pending", 0, "active", date.today(), date.today())
                cursor.execute(sql, val)
                course_id = cursor.lastrowid
                cursor.execute("INSERT INTO mentor_course (cid, uid) VALUES (%s, %s)", (course_id, user_id))
                print("**** Course added successfully ****")
        except:
            print("There was an error in adding course.. Please try again")

    @abstractmethod
    def list_course(self):
        print("This is an abstract method.")

    @abstractmethod
    def delete_course(self):
        pass

    @abstractmethod
    def calculate_earning(self, user_id):
        pass

    # @abstractmethod
    def approve_course(self):
        pass

    def view_purchased_course(self, user_id):
        message = "There was an error in fetching the content. Please try again.."
        content = get_from_db(queries.GET_STUDENT_COURSES, (user_id,), message)
        keys = ["Name", "Duration", "Price", "Rating"]

        print("Courses you've purchased : \n")
        for row in content:
            values = [row[1], row[3], row[4], row[5]]

            result = dict(zip(keys, values))
            for key, value in result.items():
                print(key + ": ", value)
            print("***************")

        return content

    def view_course_content(self, user_id):

        content = self.view_purchased_course(user_id)
        flag = 0
        user_input = get_string_input("Enter the name of course you wish to study from : ")
        for row in content:
            if row[1].lower() == user_input.lower():
                flag = 1
                message = "There was an error in fetching the content. Please try again.."
                result = get_from_db(queries.GET_DETAILS_COURSES, (row[1],), message)
                print("**** Content Begins **** ")
                print(result[0][2])
                print("**** END **** ")
        if flag == 0:
            print("No such course exists")

    @staticmethod
    def purchase_course(user_id):

        message = "There was some error, please try again.."
        content = get_from_db(queries.GET_COURSES_STATUS, ("approved", "active"), message)
        keys = ["Name", "Duration", "Price", "Rating"]

        print("Courses available : \n")
        for row in content:
            values = [row[1], row[3], row[4], row[5]]

            result = dict(zip(keys, values))
            for key, value in result.items():
                print(key + ": ", value)
            print("***************")
        user_input = get_string_input("Enter the name of course you wish to purchase : ")
        flag = 0
        for row in content:
            if row[1].lower() == user_input.lower():
                flag = 1
                result = get_from_db(queries.PURCHASE_COURSE_UID_CID, (user_id, row[0]), message)

                if len(result) == 0 or result is None:
                    insert_into_db(queries.INSERT_STUDENT_COURSES, (user_id, row[0], date.today()), message)
                    no_of_students = get_from_db(queries.GET_NO_STUDENTS, (row[0],))

                    updated_no_of_student = no_of_students[0][0]
                    updated_no_of_student += 1
                    update_db((queries.UPDATE_NO_OF_STUDENTS, row[0]))
                    print("**** Course purchased successfully ****")
                else:
                    print("You've already purchased this course.")
        if flag == 0:
            print("No such course exists.")
        result = get_from_db(queries.GET_USER_ROLES, (user_id,))
        for row in result:
            if row[2] == 4:
                update_db(queries.UPDATE_USER_ROLES, (2, user_id))
                return
