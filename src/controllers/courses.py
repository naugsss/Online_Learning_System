"""operation related to courses"""
from datetime import date
from src.controllers.auth import Login
from src.helpers.course_enum import CourseField
from src.models.database import db
from src.configurations.config import sql_queries, prompts
from src.helpers.roles_enum import Roles

QUERIES = sql_queries
PROMPTS = prompts


class Courses:
    """Operations for Courses"""

    def add_course(self, user_id, course_name, content, duration, price):
        """add a new course

        Args:
            user_id (int): the user id of the logged in user
            course_name (string): the name of the new course
            content (string): content of the new course
            duration (int): duration of the new course
            price (int): price of the new course

        Returns:
            string: custom message, course approval request sent to admin
        """
        result = db.get_from_db(QUERIES.get("GET_DETAILS_COURSES"), (course_name,))
        if len(result) != 0:
            return PROMPTS.get("COURSE_ALREADY_EXISTS")
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
        course_id = db.insert_into_db(QUERIES.get("INSERT_COURSES"), val)
        db.insert_into_db(
            QUERIES.get("INSERT_INTO_MENTOR_COURSE"), (course_id, user_id)
        )
        return PROMPTS.get("COURSE_APPROVAL_REQUEST")

    def get_course_list_from_db(self, role, user_id):
        """display all the courses available

        Args:
            role (int): Role of the person, can be admin, mentor, student, visitor
            user_id (int): the user id of the logged in user

        Returns:
            list of tuples: the course list which we fetch from db
        """
        if role == Roles.ADMIN.value:
            query = QUERIES.get("GET_COURSES")
            content = db.get_from_db(query)
            return content

        if role == Roles.STUDENT.value or role == Roles.VISITOR.value:
            query = QUERIES.get("GET_COURSES_STATUS")
            content = db.get_from_db(query, ("approved", "active"))
            return content

        if role == Roles.MENTOR.value:
            content = db.get_from_db(QUERIES.get("GET_MENTOR_COURSE"), (user_id,))
            return content

    def delete_course(self, course_name):
        """admin can deactivate a course

        Args:
            course_name (string): course name entered for deactivation

        Returns:
            string: message indicating deactivation
        """
        db.update_db(QUERIES.get("UPDATE_COURSE_STATUS"), ("deactive", course_name))
        return PROMPTS.get("COURSE_DEACTIVATED")

    def approve_course(self, course_id, approval_status):
        """approve a course

        Args:
            course_id (int): id of a particular course
            approval_status (string): whether the course needs to be approved or rejected

        Returns:
            Course Status (string): whether course has been approved or rejected.
        """
        if approval_status == "approve":
            db.update_db(
                QUERIES.get("UPDATE_PENDING_APPROVAL_STATUS"), ("approved", course_id)
            )
            return PROMPTS.get("COURSE_APPROVED")

        db.delete_from_db(QUERIES.get("DELETE_FROM_MENTOR_COURSE"), (course_id,))
        db.delete_from_db(QUERIES.get("DELETE_FROM_COURSES"), (course_id,))
        return PROMPTS.get("COURSE_REJECTED")

    def view_purchased_course(self, user_id):
        """view list of purchased courses

        Args:
            user_id (int): the user id of the logged in user

        Returns:
            string:  list of purchased courses
        """
        query = QUERIES.get("GET_STUDENT_COURSES")
        content = db.get_from_db(query, (user_id,))
        return content

    def view_course_content(self, course_name):
        """view the content of the course

        Args:
            course_name (string): name of the course, entered by the user, if the user has purchased that course, content of the course is displayed, otherwise a custom message is displayed

        Returns:
            string: content of the course
        """
        result = db.get_from_db(QUERIES.get("GET_DETAILS_COURSES"), (course_name,))
        return result[0][2]

    def purchase_course(self, user_id, course_id):
        """purchase a course

        Args:
            user_id (int): the user id of the user
            course_id (_type_): id of the course to be purchased

        Returns:
            string: custom message, whether course was purchased or not
        """
        result = db.get_from_db(
            QUERIES.get("PURCHASE_COURSE_UID_CID"), (user_id, course_id)
        )

        if len(result) == 0 or result is None:
            db.insert_into_db(
                QUERIES.get("INSERT_STUDENT_COURSES"),
                (user_id, course_id, date.today()),
            )

            no_of_students = db.get_from_db(
                QUERIES.get("GET_NO_STUDENTS"), (course_id,)
            )

            if no_of_students and len(no_of_students) > 0:
                updated_no_of_student = no_of_students[0][7] + 1
                db.update_db(
                    QUERIES.get("UPDATE_NO_OF_STUDENTS"),
                    (updated_no_of_student, course_id),
                )
            else:
                return PROMPTS.get("PURCHASE_ERROR")

            Login.update_role(user_id)
            return PROMPTS.get("COURSE_PURCHASED_SUCESS")

        return PROMPTS.get("COURSE_ALREADY_PURCHASED")


def list_course_by_role(content, role=None):
    response = []
    for val in content:
        name = val[CourseField.NAME.value]
        duration = val[CourseField.DURATION.value]
        price = val[CourseField.PRICE.value]
        rating = val[CourseField.RATING.value]
        status = val[CourseField.STATUS.value]
        approval_status = val[CourseField.APPROVAL_STATUS.value]
        no_of_students = val[CourseField.NO_OF_STUDENTS.value]
        earning = no_of_students * price

        return_dict = {
            "name": name,
            "duration (in hrs.)": duration,
            "price (in Rs.)": price,
            "rating": rating,
        }

        if role == Roles.ADMIN.value:
            return_dict["approval_status"] = approval_status
            return_dict["status"] = status

        elif role == Roles.MENTOR.value:
            return_dict["no_of_students"] = no_of_students
            return_dict["earning"] = earning

        response.append(return_dict)
    return response
