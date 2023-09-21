from src.controllers.courses import Courses
from src.models.database import DatabaseConnection
from src.models.fetch_json_data import JsonData

DatabaseConnection = DatabaseConnection()
get_query = JsonData.load_data()


class Mentor(Courses):

    def add_mentor(self, user_name):
        result = DatabaseConnection.insert_into_db(get_query.get("GET_FROM_AUTHENTICATION"), (user_name,))
        DatabaseConnection.update_db(get_query.get("UPDATE_INTO_USER_ROLES"), (3, result[0][3]))
        return "**** Mentor added successfully ****"
