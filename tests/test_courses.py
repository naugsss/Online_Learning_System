import sys
import os
from datetime import date
from io import StringIO
from unittest.mock import patch, Mock
from src.controllers.courses import Courses, input_study_course_name, list_course_in_tabular_form
from src.models.database import DatabaseConnection
import unittest
from src.models.fetch_json_data import JsonData

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

get_query = JsonData.load_data()
DatabaseConnection = DatabaseConnection()


class TestCourses(unittest.TestCase):

    @patch("src.controllers.courses.DatabaseConnection.insert_into_db")
    @patch("src.controllers.courses.DatabaseConnection.get_course_id")
    def test_add_course(self, mock_insert_into_db, mock_get_course_id):
        mock_get_course_id.return_value = None
        mock_insert_into_db.return_value = None

        course = Courses()

        user_id = 1
        course_name = "angular"
        content = "This course teaches you the basics of Python programming."
        duration = 10
        price = 100
        expected_output = "Course approval request sent to admin."
        response = course.add_course(user_id, course_name, content, duration, price)
        self.assertEqual(response, expected_output)

    @patch("src.controllers.courses.DatabaseConnection.update_db")
    def test_delete_course(self, mock_update_db):
        mock_update_db.return_value = None
        captured_output = StringIO()
        sys.stdout = captured_output
        course = Courses()
        course.delete_course("master dsa")
        sys.stdout = sys.__stdout__
        printed_output = captured_output.getvalue()
        self.assertIn("**** Course marked as deactivated successfully ****", printed_output)

    @patch("src.controllers.courses.DatabaseConnection.get_from_db")
    def test_view_purchased_course(self, mock_get_from_db):
        mock_get_from_db.return_value = [
            (1, 'Master dsa', 'dsa is awesome', 12, 1000, 4.5),
            (3, 'Java script', 'java script is amazing', 20, 2000, 5.0)
        ]
        captured_output = StringIO()
        sys.stdout = captured_output
        course = Courses()
        content = course.view_purchased_course(user_id=1)
        sys.stdout = sys.__stdout__
        printed_output = captured_output.getvalue()
        expected_output = """Courses you've purchased : 

+-------------+---------------------+------------------+----------+
| Name        |   Duration (in hrs) |   Price (in Rs.) |   Rating |
+=============+=====================+==================+==========+
| Master dsa  |                  12 |             1000 |      4.5 |
+-------------+---------------------+------------------+----------+
| Java script |                  20 |             2000 |      5   |
+-------------+---------------------+------------------+----------+
"""

        self.assertEqual(printed_output, expected_output)

        expected_content = [
            (1, 'Master dsa', 'dsa is awesome', 12, 1000, 4.5),
            (3, 'Java script', 'java script is amazing', 20, 2000, 5.0)
        ]
        self.assertEqual(content, expected_content)

    @patch("src.controllers.courses.DatabaseConnection.get_from_db")
    def test_view_course_content(self, mock_get_from_db):
        mock_get_from_db.return_value = [(1, 'Master dsa', 'Course content')]
        course = Courses()
        course_name = "Master dsa"
        result = course.view_course_content(course_name)
        self.assertEqual(result, 'Course content')

    @patch("src.controllers.courses.DatabaseConnection.insert_into_db")
    @patch("src.controllers.courses.DatabaseConnection.get_from_db")
    @patch("src.controllers.courses.DatabaseConnection.update_db")
    @patch("src.controllers.auth.Login.update_role")
    def test_purchase_course_success(self, mock_update_role, mock_update_db, mock_insert_into_db, mock_get_from_db):
        # mock_get_from_db.return_value = []
        # mock_get_from_db.side_effect = [
        #     [(1, 'Course1', 'Description1', 10, 500, 4.0, 'approved', 1, 'active', '2023-09-09 00:00:00')],
        #     [(1,)]]
        # mock_insert_into_db.return_value = None
        # mock_update_db.return_value = None
        # mock_update_role.return_value = None
        # course = Courses()
        # course.purchase_course(user_id=1, course_id=1)
        user_id = 1
        course_id = 3

        # Mock DatabaseConnection.get_from_db to return an empty result, indicating the course is not yet purchased
        mock_get_from_db.return_value = []

        # Mock DatabaseConnection.get_from_db to return a list with the updated number of students
        mock_get_no_students = Mock(return_value=[(1, 3, 'Master dsa', 5, date.today(), 10)])
        mock_get_from_db.side_effect = [mock_get_no_students, []]

        # Create an instance of YourClass
        course = Courses()

        # Act
        result = course.purchase_course(user_id, course_id)

        # Assert
        self.assertEqual(result, "Course purchased successfully")

        # Verify that the expected database and function calls were made
        mock_get_from_db.assert_called_with("PURCHASE_COURSE_UID_CID", (user_id, course_id))
        mock_insert_into_db.assert_called_with("INSERT_STUDENT_COURSES", (user_id, course_id, date.today()))
        mock_update_db.assert_called_with("UPDATE_NO_OF_STUDENTS", (11, course_id))
        mock_update_role.assert_called_with(user_id)

    @patch("src.controllers.courses.DatabaseConnection.get_from_db")
    def test_purchase_course_already_purchased(self, mock_get_from_db):
        mock_get_from_db.return_value = [(1,)]
        course = Courses()
        course.purchase_course(user_id=1, course_id=1)

    @patch("src.controllers.courses.DatabaseConnection.get_from_db")
    @patch("src.controllers.courses.DatabaseConnection.insert_into_db")
    def test_purchase_course_course_not_purchased(self, mock_insert_into_db, mock_get_from_db):
        mock_get_from_db.return_value = []
        mock_insert_into_db.return_value = None
        course = Courses()
        course.purchase_course(user_id=1, course_id=1)

    @patch('builtins.input', side_effect=['Course1'])
    def test_input_study_course_name_valid_input(self, mock_input):
        user_input = input_study_course_name()
        self.assertEqual(user_input, 'Course1')

    @patch('builtins.input', side_effect=['', 'Course2'])
    def test_input_study_course_name_empty_input_then_valid_input(self, mock_input):
        user_input = input_study_course_name()
        self.assertEqual(user_input, 'Course2')

    @patch('src.controllers.courses.DatabaseConnection.get_from_db')
    def test_list_course_in_tabular_form(self, mock_get_from_db):

        query = "SELECT * FROM courses"
        headers = ["Name", "Duration (in hrs)", "Price (in Rs.)", "Rating"]
        columns = [1, 3, 4, 5]
        params = ("approved", "active")
        mock_query_result = [
            (1, 'Course1', 'Description1', 10, 500, 4.0, 'approved', 1, 'active'),
            (2, 'Course2', 'Description2', 20, 1000, 3.5, 'approved', 1, 'active')
        ]
        mock_get_from_db.return_value = mock_query_result

        result = list_course_in_tabular_form(query, headers, "grid", columns, params)

        mock_get_from_db.assert_called_once_with(query, params)
        self.assertIn(['Course1', 10, 500, 4.0], result)
        self.assertIn(['Course2', 20, 1000, 3.5], result)
