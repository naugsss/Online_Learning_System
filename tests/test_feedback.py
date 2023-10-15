import unittest
from datetime import date
from unittest.mock import patch
from src.controllers.feedback import Feedback
from src.configurations.config import sql_queries

QUERIES = sql_queries


feedback = Feedback()


class TestFeedback(unittest.TestCase):
    @patch("src.controllers.feedback.db")
    def test_view_course_feedback_success(self, mocked_db_object):
        return_value = [
            (
                1,
                1,
                5.0,
                "Good course",
                date(2021, 9, 9),
            )
        ]
        mocked_db_object.get_from_db.return_value = return_value
        course_id = 1
        response = feedback.view_course_feedback(course_id)
        self.assertEqual(response, return_value)

    @patch("src.controllers.feedback.db")
    def test_view_course_feedback_failure(self, mocked_db_object):
        return_value = []
        mocked_db_object.get_from_db.return_value = return_value
        course_id = 10
        response = feedback.view_course_feedback(course_id)
        self.assertEqual(response, None)

    @patch("src.controllers.feedback.db")
    def test_add_course_feedback_success(self, mocked_db_object):
        return_value = None
        mocked_db_object.insert_into_db.return_value = return_value
        mocked_db_object.get_from_db.return_value = [(5.0,)]
        mocked_db_object.update_db.return_value = return_value
        course_id = 1
        rating = 5.0
        comments = "Good course"
        user_id = 1
        response = feedback.add_course_feedback(course_id, rating, comments, user_id)
        self.assertEqual(response, "Feedback added successfully")
