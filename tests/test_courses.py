import datetime
import unittest
from datetime import date
from unittest import mock
from unittest.mock import patch, Mock
from src.controllers.courses import (
    Courses,
    list_course_by_role,
)


class TestCourses(unittest.TestCase):
    @patch("src.controllers.courses.db")
    def test_add_course(self, mock_db_object):
        mock_db_object.return_value = None
        course = Courses()
        user_id = 1
        course_name = "angular"
        content = "This course teaches you the basics of Python programming."
        duration = 10
        price = 100
        expected_output = "Course approval request sent to admin."
        response = course.add_course(user_id, course_name, content, duration, price)
        self.assertEqual(response, expected_output)

    @patch("src.controllers.courses.db")
    def test_delete_course(self, mock_db_object):
        mock_db_object.return_value = "Course marked as deactivated successfully"
        course = Courses()
        response = course.delete_course("master dsa")
        expected_output = "Course marked as deactivated successfully"
        self.assertEqual(response, expected_output)

    @mock.patch("src.controllers.courses.db")
    def test_view_course_content(self, mocked_db_object):
        return_value = [
            (
                18,
                "clean code",
                "dsa is easy and awesome",
                12,
                1000,
                4.75,
                "approved",
                3,
                "active",
                datetime.datetime(2023, 9, 25, 0, 0),
                datetime.datetime(2023, 9, 25, 0, 0),
            )
        ]
        mocked_db_object.get_from_db.return_value = return_value
        course = Courses()
        course_name = "Clean code"
        result = course.view_course_content(course_name)
        self.assertEqual(result, return_value[0][2])

    @patch("src.controllers.courses.db")
    def test_purchase_course_success(self, mocked_db_object):
        mocked_db_object.get_from_db.return_value = []
        mocked_db_object.insert_into_db.return_value = None
        mocked_db_object.get_from_db.return_value = [
            (
                30,
                "dsa master ",
                "Dsa is amazing.",
                12,
                2000,
                0.0,
                "approved",
                0,
                "active",
                datetime.datetime(2023, 10, 12, 0, 0),
                datetime.datetime(2023, 10, 12, 0, 0),
            )
        ]
        mocked_db_object.update_db.return_value = None
        course = Courses()
        response = course.purchase_course(user_id=1, course_id=30)
        # print("response", response)
        expected_output = "Course purchased successfully"
        self.assertEqual(response, expected_output)

    @patch("src.controllers.courses.db")
    def test_purchase_course_already_purchased(self, mocked_db_object):
        mocked_db_object.get_from_db.return_value = [
            (23, 1, 19, datetime.datetime(2023, 10, 10, 0, 0))
        ]
        mocked_db_object.insert_into_db.return_value = None
        mocked_db_object.get_from_db.return_value = [
            (23, 1, 19, datetime.datetime(2023, 10, 10, 0, 0))
        ]
        mocked_db_object.update_db.return_value = None
        course = Courses()
        response = course.purchase_course(user_id=1, course_id=3)
        expected_output = "You've already purchased this course."
        self.assertEqual(response, expected_output)

    @patch("src.controllers.courses.db")
    def test_approve_course(self, mocked_db_object):
        mocked_db_object.return_value = None
        course = Courses()
        response = course.approve_course(1, "approved")
        self.assertEqual(response, "Course rejected")

    @patch("src.controllers.courses.db")
    def test_view_purchased_course(self, mocked_db_object):
        return_value = [
            (
                18,
                "clean code",
                "dsa is easy and awesome",
                12,
                1000,
                4.75,
                "approved",
                3,
                "active",
                datetime.datetime(2023, 9, 25, 0, 0),
                datetime.datetime(2023, 9, 25, 0, 0),
                8,
                1,
                18,
                datetime.datetime(2023, 9, 25, 0, 0),
            ),
            (
                3,
                "Java script",
                "java script is amazing",
                20,
                2000,
                4.79,
                "approved",
                16,
                "active",
                datetime.datetime(2023, 9, 10, 0, 0),
                datetime.datetime(2023, 9, 10, 0, 0),
                10,
                1,
                3,
                datetime.datetime(2023, 9, 25, 0, 0),
            ),
            (
                19,
                "Python",
                "let's talk about variables in python",
                36,
                1500,
                0.0,
                "approved",
                1,
                "active",
                datetime.datetime(2023, 9, 26, 0, 0),
                datetime.datetime(2023, 9, 26, 0, 0),
                23,
                1,
                19,
                datetime.datetime(2023, 10, 10, 0, 0),
            ),
        ]

        mocked_db_object.get_from_db.return_value = return_value
        course = Courses()
        response = course.view_purchased_course(1)
        self.assertEqual(response, return_value)

    @patch("src.controllers.courses.db")
    def test_list_course_success(self, mocked_db_object):
        return_value = [
            (
                18,
                "clean code",
                "dsa is easy and awesome",
                12,
                1000,
                4.75,
                "approved",
                3,
                "active",
                datetime.datetime(2023, 9, 25, 0, 0),
                datetime.datetime(2023, 9, 25, 0, 0),
            ),
            (
                3,
                "Java script",
                "java script is amazing",
                20,
                2000,
                4.79,
                "approved",
                16,
                "active",
                datetime.datetime(2023, 9, 10, 0, 0),
                datetime.datetime(2023, 9, 10, 0, 0),
            ),
            (
                19,
                "Python",
                "let's talk about variables in python",
                36,
                1500,
                0.0,
                "approved",
                1,
                "active",
                datetime.datetime(2023, 9, 26, 0, 0),
                datetime.datetime(2023, 9, 26, 0, 0),
            ),
        ]
        mocked_db_object.get_from_db.return_value = return_value
        course = Courses()
        response = course.get_course_list_from_db(1, 1)
        self.assertEqual(response, return_value)
        response = course.get_course_list_from_db(2, 1)
        self.assertEqual(response, return_value)
        response = course.get_course_list_from_db(3, 1)
        self.assertEqual(response, return_value)

    @patch("src.controllers.courses.db")
    def test_list_course_failure(self, mocked_db_object):
        return_value = []
        mocked_db_object.get_from_db.return_value = return_value
        course = Courses()
        response = course.get_course_list_from_db(1, 1)
        self.assertEqual(response, return_value)

    def test_list_course_by_admin_role(self):
        value = [
            {
                "name": "clean code",
                "duration (in hrs.)": 12,
                "price (in Rs.)": 1000,
                "rating": 4.75,
                "approval_status": "approved",
                "status": "active",
            }
        ]

        return_value = [
            (
                18,
                "clean code",
                "dsa is easy and awesome",
                12,
                1000,
                4.75,
                "approved",
                3,
                "active",
                datetime.datetime(2023, 9, 25, 0, 0),
                datetime.datetime(2023, 9, 25, 0, 0),
            )
        ]
        response = list_course_by_role(return_value, 1)
        self.assertEqual(response, value)

    def test_list_course_by_student_role(self):
        value = [
            {
                "name": "clean code",
                "duration (in hrs.)": 12,
                "price (in Rs.)": 1000,
                "rating": 4.75,
            }
        ]

        return_value = [
            (
                18,
                "clean code",
                "dsa is easy and awesome",
                12,
                1000,
                4.75,
                "approved",
                3,
                "active",
                datetime.datetime(2023, 9, 25, 0, 0),
                datetime.datetime(2023, 9, 25, 0, 0),
            )
        ]
        response = list_course_by_role(return_value, 2)
        self.assertEqual(response, value)

    def test_list_course_by_mentor_role(self):
        value = [
            {
                "name": "clean code",
                "duration (in hrs.)": 12,
                "price (in Rs.)": 1000,
                "rating": 4.75,
                "no_of_students": 3,
                "earning": 3000,
            }
        ]

        return_value = [
            (
                18,
                "clean code",
                "dsa is easy and awesome",
                12,
                1000,
                4.75,
                "approved",
                3,
                "active",
                datetime.datetime(2023, 9, 25, 0, 0),
                datetime.datetime(2023, 9, 25, 0, 0),
            )
        ]
        response = list_course_by_role(return_value, 3)
        self.assertEqual(response, value)
