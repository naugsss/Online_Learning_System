"""Operation related to mentor"""
from src.controllers.courses import Courses
from src.models.database import db
from src.helpers.roles_enum import Roles
from src.configurations.config import sql_queries, prompts

PROMPTS = prompts
QUERIES = sql_queries


class Mentor(Courses):
    def add_mentor(self, user_name):
        """add a new mentor

        Args:
            user_name (string): username of the user, to be made a mentor

        Returns:
            string: custom message, whether the Mentor was added or not
        """

        is_valid_username = db.get_from_db(
            QUERIES.get("GET_FROM_AUTHENTICATION"), (user_name,)
        )
        if is_valid_username:
            user_id = is_valid_username[0][3]
            user_role = db.get_from_db(QUERIES.get("GET_USER_ROLES"), (user_id,))
            # if user_role[0][2] == Roles.MENTOR.value:
            #     return PROMPTS.get("ALREADY_A_MENTOR")

            result = db.insert_into_db(
                QUERIES.get("GET_FROM_AUTHENTICATION"), (user_name,)
            )
            # print("result", result)
            # result [(6, 'sgoyal', '5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5', 5, datetime.datetime(2023, 9, 10, 0, 0))]
            db.update_db(
                QUERIES.get("UPDATE_INTO_USER_ROLES"),
                (Roles.MENTOR.value, result[0][3]),
            )
            return PROMPTS.get("MENTOR_ADDED_SUCESS")
        return PROMPTS.get("NO_SUCH_USERNAME")
