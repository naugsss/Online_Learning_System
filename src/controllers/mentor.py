from controllers.courses import Courses
from models.database import DatabaseConnection
from models.fetch_json_data import JsonData

DatabaseConnection = DatabaseConnection()
get_query = JsonData.load_data()


class Mentor(Courses):
    def add_mentor(self, user_name):
        is_valid_username = DatabaseConnection.get_from_db(
            get_query.get("GET_FROM_AUTHENTICATION"), (user_name,)
        )
        if is_valid_username:
            user_id = is_valid_username[0][3]
            user_role = DatabaseConnection.get_from_db(
                get_query.get("GET_USER_ROLES"), (user_id,)
            )
            print(user_role)
            if user_role[0][2] == 3:
                return "This person is already a mentor"
            result = DatabaseConnection.insert_into_db(
                get_query.get("GET_FROM_AUTHENTICATION"), (user_name,)
            )
            DatabaseConnection.update_db(
                get_query.get("UPDATE_INTO_USER_ROLES"), (3, result[0][3])
            )
            return "Mentor added successfully"
        return "No such username exists."
