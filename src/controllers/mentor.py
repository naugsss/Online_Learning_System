from src.controllers.courses import Courses
from src.helpers.inputs_and_validations import get_string_input
from src.models.database import DatabaseConnection
from src.utils import queries

DatabaseConnection = DatabaseConnection()


class Mentor(Courses):

    def add_mentor(self):
        user_name = get_string_input("Enter the username of the user whom you wish to make admin : ")
        result = DatabaseConnection.insert_into_db(queries.GET_FROM_AUTHENTICATION, (user_name,))
        DatabaseConnection.update_db(queries.UPDATE_INTO_USER_ROLES, (3, result[0][3]))
        print("**** Mentor added successfully ****")
