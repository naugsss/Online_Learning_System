from src.controllers.courses import Courses
from src.controllers.earning import Earning
from src.controllers.faq import Faq
from src.controllers.feeback import Feedback
from src.controllers.mentor import Mentor
from src.controllers.student import Student

student = Student()
mentor = Mentor()
feedback = Feedback()
course = Courses()
faq = Faq()
earning = Earning()

admin_menu = """
    Choose an operation from the following : 
        1. View student details. 
        2. View feedback of courses. 
        3. Add a mentor. 
        4. List courses. 
        5. Delete course. 
        6. List earning of all mentors. 
        7. exit. 
"""
student_menu = """
    Choose an operation from the following : 
        1. list all courses. 
        2. Purchase course. 
        3. My learnings. 
        4. View feedback. 
        5. Add feedback. 
        6. exit. 
"""

mentor_menu = """
    Choose an operation from the following :
        1. Add course. 
        2. Calculate earning. 
        3. List all course.
        4. List my course
        5. View feedback. 
        6. Add FAQ. 
        7. View FAQ.
        8. exit. 
"""

visitor_menu = """
    Choose an operation from the following : 
        1. List all courses. 
        2. View FAQ. 
        3. Purchase course. 
        4. View feedback. 
        5. exit. 
"""


def prompt_admin_menu(role, user_id):
    print(admin_menu)
    try:
        user_input = input_choice()
        while user_input != 7:
            if user_input == 1:
                student.view_student_details()
            elif user_input == 2:
                feedback.view_feedback(role)
            elif user_input == 3:
                mentor.add_mentor()
            elif user_input == 4:
                course.list_course(role, user_id)
            elif user_input == 5:
                course.delete_course(user_id)
            elif user_input == 6:
                earning.calculate_all_mentor_earning()
            else:
                print("You entered wrong choice, please try again.. ")
            print(admin_menu)
            user_input = input_choice()

    except:
        print("You entered a wrong choice, please try again ...")
        prompt_admin_menu(role, user_id)


def prompt_student_menu(role, user_id):
    print(student_menu)
    try:
        user_input = input_choice()
        while user_input != 6:
            if user_input == 1:
                course.list_course(role, user_id)
            elif user_input == 2:
                student.purchase_course(user_id)
            elif user_input == 3:
                student.view_course_content(user_id)
            elif user_input == 4:
                feedback.view_feedback(role)
            elif user_input == 5:
                print("Calling add feedback function : ")
                feedback.add_feedback(user_id)
            else:
                print("You entered wrong choice, please try again.. ")
            print(student_menu)
            user_input = input_choice()

    except:
        print("You entered a wrong choice, please try again ...")
        prompt_student_menu(role, user_id)


def prompt_mentor_menu(role, user_id):
    print(mentor_menu)
    try:
        user_input = input_choice()

        while user_input != 8:
            if user_input == 1:
                mentor.add_course(user_id)
            elif user_input == 2:
                earning.calculate_mentor_earning(user_id)
            elif user_input == 3:
                mentor.list_course(2, user_id)
            elif user_input == 4:
                mentor.list_course(3, user_id)
            elif user_input == 5:
                feedback.view_feedback(role)
            elif user_input == 6:
                faq.add_faq(user_id)
            elif user_input == 7:
                faq.view_faq(user_id)
            else:
                print("You entered wrong choice, please try again.. ")
            print(mentor_menu)
            user_input = input_choice()

    except:
        print("You entered a wrong choice, please try again ...")
        prompt_mentor_menu(role, user_id)


def prompt_visitor_menu(role, user_id):
    print(visitor_menu)
    try:
        user_input = input_choice()
        while user_input != 5:
            if user_input == 1:
                course.list_course(role, user_id)
            elif user_input == 2:
                faq.view_faq(user_id)
            elif user_input == 3:
                course.purchase_course(user_id)
                return
            elif user_input == 4:
                feedback.view_feedback(role)
            else:
                print("You entered wrong choice, please try again.. ")
            print(visitor_menu)
            user_input = input_choice()

    except:
        print("You entered a wrong choice, please try again ...")
        prompt_visitor_menu(role, user_id)


def input_choice():
    user_input = int(input("Please enter your choice : "))
    if user_input <= 0:
        print("input cannot be less than 0.. please try again. ")
        return input_choice()
    elif user_input > 0:
        return user_input
    else:
        print("Please enter valid number...")
        return input_choice()
