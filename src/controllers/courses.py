from datetime import date
from controllers.auth import Login
from models.database import db
from models.fetch_json_data import JsonData
from helpers.roles_enum import Roles

get_query = JsonData.load_data()


class Courses:
    def add_course(self, user_id, course_name, content, duration, price):
        result = db.get_from_db(get_query.get("GET_DETAILS_COURSES"), (course_name,))
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
        course_id = db.get_course_id(get_query.get("INSERT_COURSES"), val)
        db.insert_into_db(
            "INSERT INTO mentor_course (cid, uid) VALUES (%s, %s)", (course_id, user_id)
        )
        return "Course approval request sent to admin."

    def list_course(self, role, user_id):
        if role == Roles.ADMIN.value:
            query = get_query.get("GET_COURSES")
            content = db.get_from_db(query)
            return content

        elif role == Roles.STUDENT.value or role == Roles.VISITOR.value:
            query = get_query.get("GET_COURSES_STATUS")
            content = db.get_from_db(query, ("approved", "active"))
            return content

        elif role == Roles.MENTOR.value:
            content = db.get_from_db(get_query.get("GET_MENTOR_COURSE"), (user_id,))
            values = []
            for row in content:
                values.append(
                    [row[4], row[6], row[7], row[8], row[10], row[7] * row[10]]
                )
                # variables bna bna ke --> enum
            return values

    def delete_course(self, course_name):
        # try catch block
        db.update_db(get_query.get("UPDATE_COURSE_STATUS"), ("deactive", course_name))
        return "Course marked as deactivated successfully"

    def approve_course(self, course_id, approval_status):
        if approval_status == "approve":
            db.update_db(
                get_query.get("UPDATE_PENDING_APPROVAL_STATUS"), ("approved", course_id)
            )
            return "Course approved successfully"
        else:
            db.delete_from_db(get_query.get("DELETE_FROM_MENTOR_COURSE"), (course_id,))
            db.delete_from_db(get_query.get("DELETE_FROM_COURSES"), (course_id,))
            return "Course rejected"

    def view_purchased_course(self, user_id):
        query = get_query.get("GET_STUDENT_COURSES")
        content = db.get_from_db(query, (user_id,))
        return content

    def view_course_content(self, course_name):
        result = db.get_from_db(get_query.get("GET_DETAILS_COURSES"), (course_name,))
        return result[0][2]

    def purchase_course(self, user_id, course_id):
        result = db.get_from_db(
            get_query.get("PURCHASE_COURSE_UID_CID"), (user_id, course_id)
        )
        if len(result) == 0 or result is None:
            db.insert_into_db(
                get_query.get("INSERT_STUDENT_COURSES"),
                (user_id, course_id, date.today()),
            )

            no_of_students = db.get_from_db(
                get_query.get("GET_NO_STUDENTS"), (course_id,)
            )

            if no_of_students and len(no_of_students) > 0:
                updated_no_of_student = no_of_students[0][7] + 1
                db.update_db(
                    get_query.get("UPDATE_NO_OF_STUDENTS"),
                    (updated_no_of_student, course_id),
                )
            else:
                return "There was some error while purchasing the course, please try again."

            Login.update_role(user_id)
            return "Course purchased successfully"
        else:
            return "You've already purchased this course."
