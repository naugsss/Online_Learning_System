from src.controllers.courses import Courses
from src.helpers.inputs_and_validations import get_string_input
from src.models.database import DatabaseConnection
from src.models.fetch_json_data import JsonData

DatabaseConnection = DatabaseConnection()
get_query = JsonData.load_data()


class Mentor(Courses):

    def add_mentor(self):
        user_name = get_string_input("Enter the username of the user whom you wish to make mentor : ")
        result = DatabaseConnection.insert_into_db(get_query.get("GET_FROM_AUTHENTICATION"), (user_name,))
        DatabaseConnection.update_db(get_query.get("UPDATE_INTO_USER_ROLES"), (3, result[0][3]))
        print("**** Mentor added successfully ****")
