import re
from tabulate import tabulate
from datetime import date
from src.models.database import DatabaseConnection
from src.utils import queries

DatabaseConnection = DatabaseConnection()


class Courses:

    def __init__(self):
        self.course_name = None
        self.content = None
        self.duration = None
        self.price = None

    def add_course(self, user_id):
        self.course_name = input_course_name()
        is_valid_course_name = DatabaseConnection.get_from_db(queries.GET_DETAILS_COURSES, (self.course_name,))
        if is_valid_course_name:
            print("Same name course already exists. Please enter a different name.")
            return
        self.content = input_course_content()
        self.duration = input_course_duration()
        self.price = input_course_price()

        query = "SELECT * FROM courses WHERE name = %s"
        val = (self.course_name,)
        result = DatabaseConnection.get_course_id(query, val)
        if result != 0:
            print("Another course with the same name already exists. Please try again.")
            return
        query = "INSERT INTO courses (name, content, duration, price, avg_rating, approval_status, no_of_students, status, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (
            self.course_name, self.content, self.duration, self.price, 0, "pending", 0, "active", date.today(),
            date.today())
        course_id = DatabaseConnection.get_course_id(query, val)
        DatabaseConnection.insert_into_db("INSERT INTO mentor_course (cid, uid) VALUES (%s, %s)", (course_id, user_id))
        print("**** Course approval request sent to admin. ****")

    def list_course(self, role, user_id):
        if role == 1:
            content = DatabaseConnection.get_from_db(queries.GET_COURSES, ("approved",))
            print("Courses available : \n")
            table = [(name, duration, price, rating, status) for (_, name, _, duration, price, rating, _, _, status, *_)
                     in
                     content]
            headers = ["Name", "Duration (in hrs)", "Price (in Rs.)", "Rating", "Status"]
            table_str = tabulate(table, headers=headers, tablefmt="grid")
            print(table_str)

        elif role == 2:
            content = DatabaseConnection.get_from_db(queries.GET_COURSES_STATUS, ("approved", "active"))
            if len(content) == 0:
                print("No course exists.")
            else:
                print("Courses available : \n")
                table = [(name, duration, price, rating) for (_, name, _, duration, price, rating, *_) in content]
                headers = ["Name", "Duration (in hrs)", "Price (in Rs.)", "Rating"]
                table_str = tabulate(table, headers=headers, tablefmt="grid")
                print(table_str)
                return content
        elif role == 3:
            content = DatabaseConnection.get_from_db(queries.GET_MENTOR_COURSE, (user_id,))
            values = []
            total_earning = 0
            if len(content) == 0 or content is None:
                print("You haven't made any course till now.")
                return
            for row in content:
                total_earning += row[7]*row[10]
                values.append([row[4], row[6], row[7], row[8], row[10], row[7]*row[10]])

            print(tabulate(values,
                           headers=["Course Name", "Duration (in hrs) ", "Price (in Rs.)", "Rating", "No. of students enrolled",
                                    "Earning"], tablefmt="grid"))
            print("Your total earning is : Rs. ", total_earning)

        else:
            content = DatabaseConnection.get_from_db(queries.GET_COURSES_STATUS, ("approved", "active"))
            table = [(name, duration, price, rating) for (_, name, _, duration, price, rating, *_) in content]
            headers = ["Name", "Duration (in hrs)", "Price (in Rs.)", "Rating"]
            table_str = tabulate(table, headers=headers, tablefmt="grid")
            print(table_str)
            return content

    def delete_course(self, user_id):
        content = self.list_course(2, user_id)
        user_input = input_course_name()
        is_valid_course = False
        for row in content:
            if row[1].lower() == user_input.lower():
                is_valid_course = True
                DatabaseConnection.update_db(queries.UPDATE_COURSE_STATUS, ("deactive", row[1]))
                print("**** Course marked as deactivated successfully ****")
                break
        if not is_valid_course:
            print("No such course exists, please try again")

    def approve_course(self):
        result = DatabaseConnection.get_from_db(queries.GET_COURSES_STATUS, ("pending", "active"))
        pending_course_count = 0
        if len(result) > 0:
            pending_course_count = result[0][0]
        if pending_course_count > 0:
            print("**************************")
            print("Pending Notification : ")
            result = DatabaseConnection.get_from_db(queries.PENDING_STATUS, ("pending",))
            print("Course details : \n")

            table = [(name, duration, price) for (_, name, _, duration, price, *_) in result]
            headers = ["Name", "Duration (in months)", "Price"]
            table_str = tabulate(table, headers=headers, tablefmt="grid")
            print(table_str)

            for row in result:
                approve_reject_input = get_approve_reject_input()
                if approve_reject_input == "approve":
                    DatabaseConnection.update_db(queries.UPDATE_PENDING_APPROVAL_STATUS, ("approved", row[0]))
                    print("**** Course approved successfully ****")
                else:
                    DatabaseConnection.delete_from_db(queries.DELETE_FROM_MENTOR_COURSE, (row[0],))
                    DatabaseConnection.delete_from_db(queries.DELETE_FROM_COURSES, (row[0],))
                    print("**** Course rejected ****")
            pending_course_count -= 1

    def view_purchased_course(self, user_id):
        content = DatabaseConnection.get_from_db(queries.GET_STUDENT_COURSES, (user_id,))

        print("Courses you've purchased : \n")
        table = [(name, duration, price, rating) for (_, name, _, duration, price, rating, *_) in content]
        headers = ["Name", "Duration (in hrs)", "Price (in Rs.)", "Rating"]
        table_str = tabulate(table, headers=headers, tablefmt="grid")
        print(table_str)

        return content

    def view_course_content(self, user_id):

        content = self.view_purchased_course(user_id)
        is_valid_course = False
        user_input = input_study_course_name()
        for row in content:
            if row[1].lower() == user_input.lower():
                is_valid_course = True
                result = DatabaseConnection.get_from_db(queries.GET_DETAILS_COURSES, (row[1],))
                print("**** Content Begins **** ")
                print(result[0][2])
                print("**** END **** ")
        if not is_valid_course:
            print("No such course exists")

    @staticmethod
    def purchase_course(user_id):

        content = DatabaseConnection.get_from_db(queries.GET_COURSES_STATUS, ("approved", "active"))

        print("Courses available : \n")
        table = [(name, duration, price, rating) for (_, name, _, duration, price, rating, *_) in content]
        headers = ["Name", "Duration (in hrs)", "Price (in Rs.)", "Rating"]
        table_str = tabulate(table, headers=headers, tablefmt="grid")
        print(table_str)
        user_input = input_purchase_course_name()
        is_valid_course = False
        for row in content:
            if row[1].lower() == user_input.lower():
                is_valid_course = True
                result = DatabaseConnection.get_from_db(queries.PURCHASE_COURSE_UID_CID, (user_id, row[0]))
                if len(result) == 0 or result is None:
                    DatabaseConnection.insert_into_db(queries.INSERT_STUDENT_COURSES, (user_id, row[0], date.today()))
                    no_of_students = DatabaseConnection.get_from_db(queries.GET_NO_STUDENTS, (row[0],))

                    updated_no_of_student = no_of_students[0][7]
                    updated_no_of_student += 1
                    DatabaseConnection.update_db(queries.UPDATE_NO_OF_STUDENTS, (updated_no_of_student, row[0]))
                    print("\n**** Course purchased successfully ****")
                else:
                    print("\nYou've already purchased this course.")
        if not is_valid_course:
            print("No such course exists.")
        result = DatabaseConnection.get_from_db(queries.GET_USER_ROLES, (user_id,))
        for row in result:
            if row[2] == 4:
                DatabaseConnection.update_db(queries.UPDATE_USER_ROLES, (2, user_id))
                return


def input_course_name():
    user_input = input("Enter name of course : ")
    user_input = user_input.strip()
    regex = "^[A-Za-z0-9- ]+$"
    if not re.fullmatch(regex, user_input) or user_input == '':
        print("Please enter valid characters.")
        user_input = input_course_name()

    return user_input


def input_course_content():
    try:
        user_input = input("Enter content of course : ")
        if user_input.strip() == '':
            print("Input cannot be empty. Please try again.")
            user_input = input_course_content()
        return user_input
    except:
        print("Wrong input made... please try again. ")
        return input_course_content()


def get_approve_reject_input():
    try:
        user_input = input("Do you want to approve or reject this course : ")
        if user_input.strip() == '':
            print("Input cannot be empty. Please try again.")
            user_input = get_approve_reject_input()
        return user_input
    except:
        print("Wrong input made... please try again. ")
        return get_approve_reject_input()


def input_course_duration():
    user_input = int(input("Enter duration of course (in hours) : "))
    if user_input <= 0:
        print("input cannot be less than 0.. please try again. ")
        return input_course_duration()
    elif user_input > 0:
        return user_input
    else:
        print("Enter duration of course (in hours) : ")
        return input_course_duration()


def input_course_price():
    user_input = int(input("Enter price of course (in Rs.) : "))
    if user_input <= 0:
        print("input cannot be less than 0.. please try again. ")
        return input_course_price()
    elif user_input > 0:
        return user_input
    else:
        print("Please enter price of course (in Rs.) : ")
        return input_course_price()


def input_study_course_name():
    try:
        user_input = input("Enter the name of course you wish to study from : ")
        if user_input.strip() == '':
            print("Input cannot be empty. Please try again.")
            user_input = input_study_course_name()
        return user_input
    except:
        print("Wrong input made... please try again. ")
        return input_study_course_name()


def input_purchase_course_name():
    try:
        user_input = input("Enter the name of course you wish to purchase : ")
        if user_input.strip() == '':
            print("Input cannot be empty. Please try again.")
            user_input = input_study_course_name()
        return user_input
    except:
        print("Wrong input made... please try again. ")
        return input_study_course_name()
