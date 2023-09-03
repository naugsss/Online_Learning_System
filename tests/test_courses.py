import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import unittest
from unittest import mock

import src.controllers.auth
from src.controllers.courses import Courses
from src.models.database import DatabaseConnection
from src.utils import queries
import unittest


class AddCourseTest(unittest.TestCase):
    def test_add_course_successfully(self):
        course = Courses()
        course_name = "Python for Beginners"
        content = "This is a test content"
        duration = 3
        price = 1000

        course.add_course(2)

        self.assertEqual(DatabaseConnection.get_from_db(queries.GET_COURSES_STATUS, ("pending", "active"))[0][0], 1)

    def test_add_course_with_duplicate_course_name(self):
        course = Courses()

        course_name = "Python for Beginners"
        content = "This is a test content"
        duration = 3
        price = 1000
        course.add_course(2)

        with self.assertRaises(Exception):
            course.add_course(course_name, content, duration, price)

    def test_add_course_with_invalid_course_name(self):
        course = Courses()

        course_name = ""
        content = "This is a test content"
        duration = 3
        price = 1000

        with self.assertRaises(Exception):
            course.add_course(course_name, content, duration, price)

    def test_add_course_with_invalid_duration(self):
        course = Courses()

        course_name = "Python for Beginners"
        content = "This is a test content"
        duration = 8
        price = 1000

        with self.assertRaises(Exception):
            course.add_course(course_name, content, duration, price)

    def test_add_course_with_invalid_price(self):
        course = Courses()
        course_name = "Python for Beginners"
        content = "This is a test content"
        duration = 3
        price = -1000

        with self.assertRaises(Exception):
            course.contentadd_course(course_name, content, duration, price)


class TestCourses(unittest.TestCase):
    # def test_add_course(self):
    #     course = Courses()
    #
    #     course.add_course(user_id=10)
    #
    #     assert course.course_name == "abcd"
    #     assert course.content == "clean code is a good practice to follow"
    #     assert course.duration == 12
    #     assert course.price == 1000

    # def test_approve_course_with_pending_course(self):
    #     pending_course_count = 0
    #
    #     course = Courses()
    #
    #     course.add_course(2)
    #     course.approve_course()
    #
    #     # self.assertEqual(pending_course_count, 0)
    #     self.assertEqual(DatabaseConnection.get_from_db(queries.GET_COURSES_STATUS, ("pending", "active"))[0][0], 0)
    #     self.assertEqual(DatabaseConnection.get_from_db(queries.GET_COURSES_STATUS, ("approved",))[0][0], 1)
    #
    # @mock.patch("src.controllers.courses.approve_course")
    # def test_approve_course_without_pending_course(self, mock_approve_course):
    #     mock_approve_course.return_value = (
    #
    #     )
    #     pending_course_count = 0
    #     course = Courses()
    #     course.approve_course()
    #
    #     self.assertEqual(pending_course_count, 0)
    #     self.assertEqual(DatabaseConnection.get_from_db(queries.GET_COURSES_STATUS, ("pending", "active"))[0][0], 0)
    #     self.assertEqual(DatabaseConnection.get_from_db(queries.GET_COURSES_STATUS, ("approved",))[0][0], 0)

    def setUp(self):
        self.instance = src.controllers.auth.Login.validate_user
        # self.instance = auth()
    @mock.patch("src.controllers.auth.Login.validate_user")
    def test_add_user_details(self, mock_validate_user):

        mock_validate_user.return_value = None

        self.instance.username = "naugs"
        self.instance.password = "1234"

        result = self.instance.validate_user(self, self.instance.username, self.instance.password)
        self.assertEqual(result, mock_validate_user)
