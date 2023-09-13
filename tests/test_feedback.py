import sys
import unittest
from datetime import date
from io import StringIO
from unittest.mock import patch
from src.controllers.feedback import Feedback
from src.models.database import DatabaseConnection
from src.models.fetch_json_data import JsonData

DatabaseConnection = DatabaseConnection()

feedback = Feedback()
get_query = JsonData.load_data()


class TestFeedback(unittest.TestCase):

    @patch("src.controllers.courses.DatabaseConnection.get_from_db")
    def test_view_course_feedback(self, mock_get_from_db):
        mock_get_from_db.return_value = None
        captured_output = StringIO()
        sys.stdout = captured_output
        response = feedback.view_course_feedback(course_id=1)
        self.assertEqual(response, None)
        sys.stdout = sys.__stdout__
        printed_output = captured_output.getvalue()

        self.assertIn("+----------+-------------+", printed_output)
        self.assertIn("|   Rating | Comment     |", printed_output)
        self.assertIn("+==========+=============+", printed_output)
        self.assertIn("|      4.5 | good course |", printed_output)
        self.assertIn("+----------+-------------+", printed_output)

    @patch("src.controllers.feedback.DatabaseConnection.insert_into_db")
    @patch("src.controllers.feedback.date")
    def test_add_course_feedback(self, mock_date, mock_db_connection):
        mock_db_instance = mock_db_connection.return_value
        mock_date.today.return_value = date(2023, 9, 10)

        feedback = Feedback()

        course_id = 1
        rating = 4.5
        comments = "Good course"
        user_id = 123

        feedback.add_course_feedback(course_id, rating, comments, user_id)

        mock_db_instance.insert_into_db.assert_called_once_with(
            "INSERT_INTO_COURSE_FEEDBACK",
            ((course_id, user_id, rating, comments, date(2023, 9, 10)),)
        )
        mock_db_instance.get_from_db.assert_called_once_with(
            "GET_AVG_RATING_COURSE_FEEDBACK",
            (course_id,)
        )
        mock_db_instance.update_db.assert_called_once_with(
            "UPDATE_AVG_RATING",
            (4.5, course_id)
        )