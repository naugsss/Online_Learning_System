from datetime import date
from controllers.courses import Courses
from models.database import db
from models.fetch_json_data import JsonData

course = Courses()
get_query = JsonData.load_data()


class Feedback:
    def view_course_feedback(self, course_id):
        result = db.get_from_db(get_query.get("GET_FROM_COURSE_FEEDBACK"), (course_id,))
        if len(result) != 0:
            return result
        else:
            return None

    def add_course_feedback(self, course_id, rating, comments, user_id):
        val = (course_id, user_id, rating, comments, date.today())
        db.insert_into_db(get_query.get("INSERT_INTO_COURSE_FEEDBACK"), val)

        ratings = db.get_from_db(
            get_query.get("GET_AVG_RATING_COURSE_FEEDBACK"), (course_id,)
        )
        ratings = round(ratings[0][0], 2)

        db.update_db(get_query.get("UPDATE_AVG_RATING"), (ratings, course_id))
        return "Feedback added successfully"
