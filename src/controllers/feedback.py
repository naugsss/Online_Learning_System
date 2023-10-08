from datetime import date
from tabulate import tabulate
from controllers.courses import Courses
from models.database import DatabaseConnection
from models.fetch_json_data import JsonData

course = Courses()
DatabaseConnection = DatabaseConnection()
get_query = JsonData.load_data()


class Feedback:
    def view_course_feedback(self, course_id):
        result = DatabaseConnection.get_from_db(
            get_query.get("GET_FROM_COURSE_FEEDBACK"), (course_id,)
        )
        if len(result) != 0:
            table = [(rating, comment) for (_, _, _, rating, comment, *_) in result]
            headers = ["Rating", "Comment"]
            table_str = tabulate(table, headers=headers, tablefmt="grid")
            print(table_str)
            return result
        else:
            return None

    def add_course_feedback(self, course_id, rating, comments, user_id):
        val = (course_id, user_id, rating, comments, date.today())
        DatabaseConnection.insert_into_db(
            get_query.get("INSERT_INTO_COURSE_FEEDBACK"), val
        )

        ratings = DatabaseConnection.get_from_db(
            get_query.get("GET_AVG_RATING_COURSE_FEEDBACK"), (course_id,)
        )
        ratings = round(ratings[0][0], 2)

        DatabaseConnection.update_db(
            get_query.get("UPDATE_AVG_RATING"), (ratings, course_id)
        )
        return "Feedback added successfully"
