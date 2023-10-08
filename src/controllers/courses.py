from tabulate import tabulate
from datetime import date
from controllers.auth import Login
from models.database import DatabaseConnection
from models.fetch_json_data import JsonData

DatabaseConnection = DatabaseConnection()
get_query = JsonData.load_data()


class Courses:
    def __init__(self):
        self.course_name = None
        self.content = None
        self.duration = None
        self.price = None

    def add_course(self, user_id, course_name, content, duration, price):
        result = DatabaseConnection.get_from_db(
            get_query.get("GET_DETAILS_COURSES"), (course_name,)
        )
        if len(result) != 0:
            return "Another course with the same name already exists. Please try again."

        val = (
            course_name,
            content,
            duration,
            price,
            0,
            "pending",
            0,
            "active",
            date.today(),
            date.today(),
        )
        course_id = DatabaseConnection.get_course_id(
            get_query.get("INSERT_COURSES"), val
        )
        DatabaseConnection.insert_into_db(
            "INSERT INTO mentor_course (cid, uid) VALUES (%s, %s)", (course_id, user_id)
        )
        return "Course approval request sent to admin."

    def list_course(self, role, user_id):
        if role == 1:
            return self.print_course_list_role_1()

        elif role == 2 or role == 4:
            return self.print_course_list_role_2_or_4()

        elif role == 3:
            return self.print_course_list_role_3(user_id)

    def delete_course(self, course_name):
        DatabaseConnection.update_db(
            get_query.get("UPDATE_COURSE_STATUS"), ("deactive", course_name)
        )
        print("Course marked as deactivated successfully")

    def approve_course(self, course_id, approval_status):
        if approval_status == "approve":
            DatabaseConnection.update_db(
                get_query.get("UPDATE_PENDING_APPROVAL_STATUS"), ("approved", course_id)
            )
            return "**** Course approved successfully ****"
        else:
            DatabaseConnection.delete_from_db(
                get_query.get("DELETE_FROM_MENTOR_COURSE"), (course_id,)
            )
            DatabaseConnection.delete_from_db(
                get_query.get("DELETE_FROM_COURSES"), (course_id,)
            )
            return "**** Course rejected ****"

    def view_purchased_course(self, user_id):
        print("Courses you've purchased : \n")
        headers = ["Name", "Duration (in hrs)", "Price (in Rs.)", "Rating"]
        query = get_query.get("GET_STUDENT_COURSES")
        included_columns = [1, 3, 4, 5]
        content = list_course_in_tabular_form(
            query, headers, "grid", included_columns, user_id
        )

        return content

    def view_course_content(self, course_name):
        result = DatabaseConnection.get_from_db(
            get_query.get("GET_DETAILS_COURSES"), (course_name,)
        )
        return result[0][2]

    def purchase_course(self, user_id, course_id):
        result = DatabaseConnection.get_from_db(
            get_query.get("PURCHASE_COURSE_UID_CID"), (user_id, course_id)
        )
        if len(result) == 0 or result is None:
            DatabaseConnection.insert_into_db(
                get_query.get("INSERT_STUDENT_COURSES"),
                (user_id, course_id, date.today()),
            )

            no_of_students = DatabaseConnection.get_from_db(
                get_query.get("GET_NO_STUDENTS"), (course_id,)
            )

            if no_of_students and len(no_of_students) > 0:
                updated_no_of_student = no_of_students[0][7] + 1
                DatabaseConnection.update_db(
                    get_query.get("UPDATE_NO_OF_STUDENTS"),
                    (updated_no_of_student, course_id),
                )
            else:
                return "Could not update the number of students."

            Login.update_role(user_id)
            return "Course purchased successfully"
        else:
            return "You've already purchased this course."

    def print_course_list_role_1(self):
        query = get_query.get("GET_COURSES")
        headers = [
            "Name",
            "Duration (in hrs)",
            "Price (in Rs.)",
            "Rating",
            "approval_status",
            "Status",
        ]
        included_columns = [1, 3, 4, 5, 6, 8]
        content = list_course_in_tabular_form(query, headers, "grid", included_columns)
        return content

    def print_course_list_role_2_or_4(self):
        print("Courses available : \n")
        query = get_query.get("GET_COURSES_STATUS")
        headers = ["Name", "Duration (in hrs)", "Price (in Rs.)", "Rating"]
        included_columns = [1, 3, 4, 5]
        content = list_course_in_tabular_form(
            query, headers, "grid", included_columns, ("approved", "active")
        )
        return content

    def print_course_list_role_3(self, user_id):
        content = DatabaseConnection.get_from_db(
            get_query.get("GET_MENTOR_COURSE"), (user_id,)
        )
        values = []
        total_earning = 0
        if len(content) == 0 or content is None:
            print("You haven't made any course till now.")
            return
        for row in content:
            total_earning += row[7] * row[10]
            values.append([row[4], row[6], row[7], row[8], row[10], row[7] * row[10]])

        print(
            tabulate(
                values,
                headers=[
                    "Course Name",
                    "Duration (in hrs) ",
                    "Price (in Rs.)",
                    "Rating",
                    "No. of students enrolled",
                    "Earning",
                ],
                tablefmt="grid",
            )
        )
        print("Your total earning is : Rs. ", total_earning)
        return values


def list_course_in_tabular_form(
    query, headers, table_format="grid", columns=None, params=None
):
    if params is None:
        params = ()
    elif not isinstance(params, tuple):
        params = (params,)

    content = DatabaseConnection.get_from_db(query, params)
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
        if user_input.strip() == "":
            print("Input cannot be empty. Please try again.")
            user_input = get_approve_reject_input(course_name)
        return user_input
    except:
        print("Wrong input made... please try again. ")
        return get_approve_reject_input(course_name)


def input_study_course_name():
    try:
        user_input = input("Enter the name of course you wish to study from : ")
        if user_input.strip() == "":
            print("Input cannot be empty. Please try again.")
            user_input = input_study_course_name()
        return user_input
    except:
        print("Wrong input made... please try again. ")
        return input_study_course_name()
