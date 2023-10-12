from enum import Enum
from src.helpers.roles_enum import Roles


class CourseField(Enum):
    NAME = 1
    DURATION = 3
    PRICE = 4
    RATING = 5
    APPROVAL_STATUS = 6
    NO_OF_STUDENTS = 7
    STATUS = 8


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
