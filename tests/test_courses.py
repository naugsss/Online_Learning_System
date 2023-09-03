import unittest
from unittest import mock

import src.controllers.auth
from src.controllers.courses import Courses
from src.models.database import DatabaseConnection
from src.utils import queries


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
