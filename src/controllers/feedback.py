from datetime import date
from src.controllers.courses import Courses
from src.models.database import db
from src.configurations.config import sql_queries, prompts


course = Courses()
QUERIES = sql_queries
PROMPTS = prompts


class Feedback:
    def view_course_feedback(self, course_id):
        """view feedback for a given course

        Args:
            course_id (int): id of a particular course

        Returns:
            string: feedback for a given course if exists, or none.
        """
        result = db.get_from_db(QUERIES.get("GET_FROM_COURSE_FEEDBACK"), (course_id,))
        if len(result) != 0:
            return result

        return None

    def add_course_feedback(self, course_id, rating, comments, user_id):
        """adding feedback for a given course, only if the user has purchased the course

        Args:
            course_id (int): if of a particular course
            rating (float): rating of a course, entered by the user
            comments (string): optional, the feedback of user
            user_id (int): id of the user who is adding the feedback

        Returns:
            string: custom message, the feedback has been added successfully.
        """
        val = (course_id, user_id, rating, comments, date.today())
        db.insert_into_db(QUERIES.get("INSERT_INTO_COURSE_FEEDBACK"), val)

        ratings = db.get_from_db(
            QUERIES.get("GET_AVG_RATING_COURSE_FEEDBACK"), (course_id,)
        )
        ratings = round(ratings[0][0], 2)

        db.update_db(QUERIES.get("UPDATE_AVG_RATING"), (ratings, course_id))
        return PROMPTS.get("FEEDBACK_ADDED_SUCESS")
