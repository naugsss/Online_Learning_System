from controllers.courses import Courses
from models.database import db
from models.fetch_json_data import JsonData
from helpers.roles_enum import Roles

get_query = JsonData.load_data()


class Mentor(Courses):
    def add_mentor(self, user_name):
        # TODO:
        # is_user_present, is_valid_username isko change krna h
        is_valid_username = db.get_from_db(
            get_query.get("GET_FROM_AUTHENTICATION"), (user_name,)
        )
        if is_valid_username:
            user_id = is_valid_username[0][3]
            user_role = db.get_from_db(get_query.get("GET_USER_ROLES"), (user_id,))
            if user_role[0][2] == Roles.MENTOR.value:
                return "This person is already a mentor"
            result = db.insert_into_db(
                get_query.get("GET_FROM_AUTHENTICATION"), (user_name,)
            )
            db.update_db(
                get_query.get("UPDATE_INTO_USER_ROLES"),
                (Roles.MENTOR.value, result[0][3]),
            )
            return "Mentor added successfully"
        return "No such username exists."
