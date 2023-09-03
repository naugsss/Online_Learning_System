import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
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

