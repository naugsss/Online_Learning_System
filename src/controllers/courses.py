from tabulate import tabulate
from datetime import date
from src.controllers.auth import Login
from src.models.database import DatabaseConnection
from src.models.fetch_json_data import JsonData

DatabaseConnection = DatabaseConnection()
get_query = JsonData.load_data()


class Courses:

    def __init__(self):
        self.course_name = None
        self.content = None
        self.duration = None
        self.price = None

    def add_course(self, user_id, course_name, content, duration, price):

        result = DatabaseConnection.get_course_id(get_query["GET_DETAILS_COURSES"], (self.course_name,))
        if result != 0:
            print("Another course with the same name already exists. Please try again.")
            return
        val = (
            course_name, content, duration, price, 0, "pending", 0, "active", date.today(),
            date.today())
        course_id = DatabaseConnection.get_course_id(get_query["INSERT_COURSES"], val)
        DatabaseConnection.insert_into_db("INSERT INTO mentor_course (cid, uid) VALUES (%s, %s)", (course_id, user_id))
        print("**** Course approval request sent to admin. ****")

    def list_course(self, role, user_id):
        if role == 1:
            query = get_query["GET_COURSES"]
            headers = ["Name", "Duration (in hrs)", "Price (in Rs.)", "Rating", "Status"]
            included_columns = [1, 3, 4, 5, 8]
            print_courses_list(query, headers, "grid", included_columns, "approved")

        elif role == 2 or role == 4:
            print("Courses available : \n")
            query = get_query["GET_COURSES_STATUS"]
            headers = ["Name", "Duration (in hrs)", "Price (in Rs.)", "Rating"]
            included_columns = [1, 3, 4, 5]
            content = print_courses_list(query, headers, "grid", included_columns, ("approved", "active"))
            return content

        elif role == 3:
            content = DatabaseConnection.get_from_db(get_query["GET_MENTOR_COURSE"], (user_id,))
            values = []
            total_earning = 0
            if len(content) == 0 or content is None:
                print("You haven't made any course till now.")
                return
            for row in content:
                total_earning += row[7] * row[10]
                values.append([row[4], row[6], row[7], row[8], row[10], row[7] * row[10]])

            print(tabulate(values,
                           headers=["Course Name", "Duration (in hrs) ", "Price (in Rs.)", "Rating",
                                    "No. of students enrolled",
                                    "Earning"], tablefmt="grid"))
            print("Your total earning is : Rs. ", total_earning)

    def delete_course(self, course_name, content):
        is_valid_course = False
        for row in content:
            if row[1].lower() == course_name.lower():
                is_valid_course = True
                DatabaseConnection.update_db(get_query["UPDATE_COURSE_STATUS"], ("deactive", row[1]))
                print("**** Course marked as deactivated successfully ****")
                break
        if not is_valid_course:
            print("No such course exists, please try again")

    def approve_course(self, course_name, pending_course_count):
        result = DatabaseConnection.get_from_db(get_query["GET_COURSES_STATUS"], ("pending", "active"))
        for row in result:
            approve_reject_input = get_approve_reject_input(course_name)
            if approve_reject_input == "approve":
                DatabaseConnection.update_db(get_query["UPDATE_PENDING_APPROVAL_STATUS"], ("approved", row[0]))
                print("**** Course approved successfully ****")
            else:
                DatabaseConnection.delete_from_db(get_query["DELETE_FROM_MENTOR_COURSE"], (row[0],))
                DatabaseConnection.delete_from_db(get_query["DELETE_FROM_COURSES"], (row[0],))
                print("**** Course rejected ****")
            pending_course_count -= 1

    def view_purchased_course(self, user_id):
        print("Courses you've purchased : \n")
        headers = ["Name", "Duration (in hrs)", "Price (in Rs.)", "Rating"]
        query = get_query["GET_STUDENT_COURSES"]
        included_columns = [1, 3, 4, 5]
        content = print_courses_list(query, headers, "grid", included_columns, user_id)
        return content

    def view_course_content(self, user_id):
        content = self.view_purchased_course(user_id)
        is_valid_course = False
        user_input = input_study_course_name()
        for row in content:
            if row[1].lower() == user_input.lower():
                is_valid_course = True
                result = DatabaseConnection.get_from_db(get_query["GET_DETAILS_COURSES"], (row[1],))
                print("**** Content Begins **** ")
                print(result[0][2])
                print("**** END **** ")
        if not is_valid_course:
            print("No such course exists")

    def purchase_course(self, user_id):
        content = self.list_course(4, user_id)
        if content is None:
            return
        user_input = input_purchase_course_name()
        is_valid_course = False
        for row in content:
            if row[1].lower() == user_input.lower():
                is_valid_course = True
                result = DatabaseConnection.get_from_db(get_query["PURCHASE_COURSE_UID_CID"], (user_id, row[0]))
                if len(result) == 0 or result is None:
                    DatabaseConnection.insert_into_db(get_query["INSERT_STUDENT_COURSES"],
                                                      (user_id, row[0], date.today()))
                    no_of_students = DatabaseConnection.get_from_db(get_query["GET_NO_STUDENTS"], (row[0],))
                    updated_no_of_student = no_of_students[0][7] + 1

                    DatabaseConnection.update_db(get_query["UPDATE_NO_OF_STUDENTS"], (updated_no_of_student, row[0]))
                    print("\n**** Course purchased successfully ****")
                    Login.update_role(user_id)
                else:
                    print("\nYou've already purchased this course.")
        if not is_valid_course:
            print("No such course exists.")
            return


def print_courses_list(query, headers, table_format="grid", columns=None, dynamic_params=None):
    if dynamic_params is None:
        dynamic_params = ()
    elif not isinstance(dynamic_params, tuple):
        dynamic_params = (dynamic_params,)

    content = DatabaseConnection.get_from_db(query, dynamic_params)
    if len(content) == 0:
        print("No course exists.")
        return
    table = []
    for content_row in content:
        row = [content_row[i] for i in columns]
        table.append(row)
    table_str = tabulate(table, headers=headers, tablefmt=table_format)
    print(table_str)
    return content


def get_approve_reject_input(course_name):
    try:
        user_input = input(f"Do you want to approve or reject {course_name} course : ")
        if user_input.strip() == '':
            print("Input cannot be empty. Please try again.")
            user_input = get_approve_reject_input(course_name)
        return user_input
    except:
        print("Wrong input made... please try again. ")
        return get_approve_reject_input(course_name)


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
            user_input = input_purchase_course_name()
        return user_input
    except:
        print("Wrong input made... please try again. ")
        return input_study_course_name()
