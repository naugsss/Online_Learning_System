from src.controllers.admin import Admin
from src.controllers.feeback import Feedback
from src.controllers.mentor import Mentor
from src.controllers.student import Student
from src.controllers.visitor import Visitor
from src.helpers.get_input import get_int_input

student = Student()
mentor = Mentor()
admin = Admin()
visitor = Visitor()
feedback = Feedback()

admin_menu = """
    print("Choose an operation from the following : ")
    print("1. View student details. ")
    print("2. View feedback of courses. ")
    print("3. Add a mentor. ")
    print("4. List courses. ")
    print("5. Delete course")
    print("6. List earning of all mentors : ")
    print("7. exit. ")
"""
student_menu = """
    print("Choose an operation from the following : ")
    print("1. list all courses. ")
    print("2. Purchase course. ")
    print("3. My learning. ")
    print("4. View feedback. ")
    print("5. Add feedback. ")
    print("6. exit. ")
"""

mentor_menu = """
    print("Choose an operation from the following : ")
    print("1. Add course. ")
    print("2. Calculate earning. ")
    print("3. View feedback. ")
    print("4. Add FAQ")
    print("5. exit. ")
"""

visitor_menu = """
    print("Choose an operation from the following : ")
    print("1. List all courses. ")
    print("2. View FAQ. ")
    print("3. Purchase course. ")
    print("4. exit. ")
"""


def prompt_admin_menu(user_id):
    print(admin_menu)
    try:
        user_input = get_int_input("Please enter your choice : ")
        while user_input != 7:
            if user_input == 1:
                student.view_student_details()
            elif user_input == 2:
                feedback.view_feedback()
            elif user_input == 3:
                mentor.add_mentor()
            elif user_input == 4:
                admin.list_course()
            elif user_input == 5:
                admin.delete_course()
            elif user_input == 6:
                admin.calculate_earning()
            else:
                print("You entered wrong choice, please try again.. ")
            print(admin_menu)
            user_input = get_int_input("Please enter your choice : ")
    except:
        print("You entered a wrong choice, please try again ...")
        prompt_admin_menu(user_id)


def prompt_student_menu(user_id):
    print(student_menu)
    try:
        user_input = get_int_input("Please enter your choice : ")
        while user_input != 6:
            if user_input == 1:
                student.list_course()
            elif user_input == 2:
                student.purchase_course(user_id)
            elif user_input == 3:
                student.view_course_content(user_id)
            elif user_input == 4:
                feedback.view_feedback()
            elif user_input == 5:
                print("Calling add feedback function : ")
                feedback.add_feedback(user_id)
            else:
                print("You entered wrong choice, please try again.. ")
            print(student_menu)
            user_input = get_int_input("Please enter your choice : ")
    except:
        print("You entered a wrong choice, please try again ...")
        prompt_student_menu(user_id)


def prompt_mentor_menu(user_id):
    print(mentor_menu)
    try:
        user_input = get_int_input("Please enter your choice : ")

        while user_input != 5:
            if user_input == 1:
                mentor.add_course(user_id)
                return
            elif user_input == 2:
                mentor.calculate_earning(user_id)
            elif user_input == 3:
                feedback.view_feedback()
            elif user_input == 4:
                feedback.add_faq(user_id)
            else:
                print("You entered wrong choice, please try again.. ")
            print(mentor_menu)
            user_input = get_int_input("Please enter your choice : ")
    except:
        print("You entered a wrong choice, please try again ...")
        prompt_mentor_menu(user_id)


def prompt_visitor_menu(user_id):
    print(visitor_menu)
    try:
        user_input = get_int_input("Please enter your choice : ")
        while user_input != 4:
            if user_input == 1:
                visitor.list_course()
            elif user_input == 2:
                feedback.view_faq()
            elif user_input == 3:
                visitor.purchase_course(user_id)
                return
            else:
                print("You entered wrong choice, please try again.. ")
            print(visitor_menu)
            user_input = get_int_input("Please enter your choice : ")
    except:
        print("You entered a wrong choice, please try again ...")
        prompt_visitor_menu(user_id)
