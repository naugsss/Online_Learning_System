from unittest import TestCase

from src.controllers.courses import Courses
from src.models.database import DatabaseConnection
from src.utils import queries


class TestCourses(TestCase):
    # def test_add_course(self):
    #     course = Courses()
    #
    #     course.add_course(user_id=10)
    #
    #     assert course.course_name == "abcd"
    #     assert course.content == "clean code is a good practice to follow"
    #     assert course.duration == 12
    #     assert course.price == 1000


    def test_approve_course_with_pending_course(self):
        # Arrange
        pending_course_count = 0

        # Act
        course = Courses()
        # Act
        course.add_course(2)
        course.approve_course()

        # Assert
        # self.assertEqual(pending_course_count, 0)
        self.assertEqual(DatabaseConnection.get_from_db(queries.GET_COURSES_STATUS, ("pending", "active"))[0][0], 0)
        self.assertEqual(DatabaseConnection.get_from_db(queries.GET_COURSES_STATUS, ("approved",))[0][0], 1)

    def test_approve_course_without_pending_course(self):
        # Arrange
        pending_course_count = 0
        course = Courses()
        # Act
        course.approve_course()

        # Assert
        self.assertEqual(pending_course_count, 0)
        self.assertEqual(DatabaseConnection.get_from_db(queries.GET_COURSES_STATUS, ("pending", "active"))[0][0], 0)
        self.assertEqual(DatabaseConnection.get_from_db(queries.GET_COURSES_STATUS, ("approved",))[0][0], 0)









