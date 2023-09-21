import re
from src.helpers.inputs_and_validations import get_string_input, get_float_input
from src.controllers.courses import Courses, list_course_in_tabular_form
from src.controllers.earning import Earning
from src.controllers.faq import Faq
from src.controllers.feedback import Feedback
from src.controllers.mentor import Mentor
from src.controllers.student import Student
from src.models.database import DatabaseConnection
from src.models.fetch_json_data import JsonData
from src.utils.menu_prompt_functions import admin_menu, student_menu, mentor_menu, visitor_menu

DatabaseConnection = DatabaseConnection()

get_query = JsonData.load_data()

student = Student()
mentor = Mentor()
feedback = Feedback()
course = Courses()
faq = Faq()
earning = Earning()


class EntryMenu:
    # def __init__(self, role, user_id):
    #     self.role = role
    #     self.user_id = user_id
    #
    #     if role == 1:
    #         self.prompt_admin_menu(role, user_id)
    #     elif role == 2:
    #         # student
    #         self.prompt_student_menu(role, user_id)
    #     elif role == 3:
    #         # mentor
    #         self.prompt_mentor_menu(role, user_id)
    #     elif role == 4:
    #         # visitor
    #         self.prompt_visitor_menu(role, user_id)

    def prompt_admin_menu(self, role, user_id):
        pending_course_count = self.check_pending_courses()
        print(pending_course_count)
        if pending_course_count > 0:
            self.list_pending_course(pending_course_count)
        print(admin_menu)
        try:
            user_input = self.input_choice()
            while user_input != 7:
                if user_input == 1:
                    student.view_student_details()
                elif user_input == 2:
                    self.view_course_feedback(role)
                elif user_input == 3:
                    mentor.add_mentor()
                elif user_input == 4:
                    course.list_course(role, user_id)
                elif user_input == 5:
                    self.input_delete_course_name(user_id)
                elif user_input == 6:
                    earning.calculate_all_mentor_earning()
                else:
                    print("You entered wrong choice, please try again.. ")
                print(admin_menu)
                user_input = self.input_choice()
        except:
            print("You entered a wrong choice, please try again ...")
            self.prompt_admin_menu(role, user_id)

    def prompt_student_menu(self, role, user_id):
        print(student_menu)
        try:
            user_input = self.input_choice()
            while user_input != 6:
                if user_input == 1:
                    course.list_course(role, user_id)
                elif user_input == 2:
                    self.list_purchasable_course(user_id)
                elif user_input == 3:
                    self.input_course_name_to_study_from(user_id)
                elif user_input == 4:
                    self.view_course_feedback(role)
                elif user_input == 5:
                    self.add_course_feedback(user_id)
                else:
                    print("You entered wrong choice, please try again.. ")
                print(student_menu)
                user_input = self.input_choice()

        except:
            print("You entered a wrong choice, please try again ...")
            self.prompt_student_menu(role, user_id)

    def prompt_mentor_menu(self, role, user_id):
        print(mentor_menu)
        try:
            user_input = self.input_choice()

            while user_input != 11:
                if user_input == 1:
                    self.input_course_details(user_id)
                elif user_input == 2:
                    earning.calculate_mentor_earning(user_id)
                elif user_input == 3:
                    mentor.list_course(2, user_id)
                elif user_input == 4:
                    mentor.list_course(3, user_id)
                elif user_input == 5:
                    self.view_course_feedback(role)
                elif user_input == 6:
                    self.input_course_faq(user_id)
                elif user_input == 7:
                    self.view_course_faq(user_id)
                elif user_input == 8:
                    self.list_purchasable_course(user_id)
                elif user_input == 9:
                    self.add_course_feedback(user_id)
                elif user_input == 10:
                    self.input_course_name_to_study_from(user_id)
                else:
                    print("You entered wrong choice, please try again.. ")
                print(mentor_menu)
                user_input = self.input_choice()

        except:
            print("You entered a wrong choice, please try again ...")
            self.prompt_mentor_menu(role, user_id)

    def prompt_visitor_menu(self, role, user_id):
        print(visitor_menu)
        try:
            user_input = self.input_choice()
            while user_input != 5:
                if user_input == 1:
                    course.list_course(role, user_id)
                elif user_input == 2:
                    self.view_course_faq(user_id)
                elif user_input == 3:
                    self.list_purchasable_course(user_id)
                elif user_input == 4:
                    self.view_course_feedback(role)
                else:
                    print("You entered wrong choice, please try again.. ")
                print(visitor_menu)
                user_input = self.input_choice()

        except:
            print("You entered a wrong choice, please try again ...")
            self.prompt_visitor_menu(role, user_id)

    def input_choice(self):
        user_input = int(input("Please enter your choice : "))
        if user_input <= 0:
            print("input cannot be less than 0.. please try again. ")
            return self.input_choice()
        elif user_input > 0:
            return user_input
        else:
            print("Please enter valid number...")
            return self.input_choice()

    def input_course_details(self, user_id):
        self.course_name = self.input_course_name()
        is_valid_course_name = DatabaseConnection.get_from_db(get_query.get("GET_DETAILS_COURSES"), (self.course_name,))
        if is_valid_course_name:
            print("Same name course already exists. Please enter a different name.")
            return
        self.content = self.input_course_content()
        self.duration = self.input_course_duration()
        self.price = self.input_course_price()

        course.add_course(user_id, self.course_name, self.content, self.duration, self.price)

    def input_course_duration(self):
        user_input = int(input("Enter duration of course (in hours) : "))
        if user_input <= 0:
            print("input cannot be less than 0.. please try again. ")
            return self.input_course_duration()
        elif user_input > 0:
            return user_input
        else:
            print("Enter duration of course (in hours) : ")
            return self.input_course_duration()

    def input_course_price(self):
        user_input = int(input("Enter price of course (in Rs.) : "))
        if user_input <= 0:
            print("input cannot be less than 0.. please try again. ")
            return self.input_course_price()
        elif user_input > 0:
            return user_input
        else:
            print("Please enter price of course (in Rs.) : ")
            return self.input_course_price()

    def input_course_name(self):
        user_input = input("Enter name of course : ")
        user_input = user_input.strip()
        regex = "^[A-Za-z0-9- ]+$"
        if not re.fullmatch(regex, user_input) or user_input == '':
            print("Please enter valid characters.")
            user_input = self.input_course_name()

        return user_input

    def input_course_content(self):
        try:
            user_input = input("Enter content of course : ")
            if user_input.strip() == '':
                print("Input cannot be empty. Please try again.")
                user_input = self.input_course_content()
            return user_input
        except:
            print("Wrong input made... please try again. ")
            return self.input_course_content()

    def input_delete_course_name(self, user_id):
        content = course.list_course(2, user_id)
        if content is None:
            return
        course_to_delete = self.input_course_name()
        is_valid_course_name, course_id = self.check_valid_course(course_to_delete, content)
        if is_valid_course_name:
            course_to_delete = is_valid_course_name
            course.delete_course(course_to_delete)

    def list_purchasable_course(self, user_id):
        content = course.list_course(4, user_id)
        if content is None:
            return
        purchase_course_name = self.input_purchase_course_name()
        is_valid_course_name, course_id = self.check_valid_course(purchase_course_name, content)
        return course_id
        # if is_valid_course_name:
        #     course.purchase_course(user_id, course_id)

    def check_valid_course(self, course_name, content):
        is_valid_course = False
        course_id = None
        for row in content:
            if row[1].lower() == course_name.lower():
                is_valid_course = True
                course_name = row[1]
                course_id = row[0]

        if not is_valid_course:
            print("No such course exists")
            return False
        else:
            return [course_name, course_id]

    def view_course_feedback(self, user_id):
        content = course.list_course(2, user_id)
        if content is None:
            return
        course_name = get_string_input("Enter the name of course you wish to view feedback of : ")
        is_valid_course_name, course_id = self.check_valid_course(course_name, content)
        if is_valid_course_name:
            feedback.view_course_feedback(course_id)

    def add_course_feedback(self, user_id):
        content = course.view_purchased_course(user_id)
        if content is None:
            return
        course_name = get_string_input("Enter the name of course you wish to add feedback of : ")
        is_valid_course_name, course_id = self.check_valid_course(course_name, content)
        print("Inside add course feedback")
        #
        # print(course_id)
        print(get_query.get("CHECK_IF_FEEDBACK_PRESENT"))
        content = DatabaseConnection.get_from_db(get_query.get("CHECK_IF_FEEDBACK_PRESENT"),(course_id,user_id))

        # print(content)
        # if content is None:
        #     print("You've already added feedback for this course")
        #     return
        if is_valid_course_name:
            self.input_course_feedback(course_id, user_id)

    def input_course_feedback(self, course_id, user_id):
        # content = DatabaseConnection.get_from_db(get_query.get("CHECK_IS_FEEDBACK_ALREADY_ADDED"), (course_id, user_id))

        print("**** Add feedback ****")
        rating = float(input("Enter rating out of 5 : "))
        while rating > 5 or rating <= 0:
            rating = get_float_input("Enter rating out of 5 : ")
            if rating > 0 and rating < 5:
                break
        comments = input("Enter any comment : ")
        if comments == "":
            comments = "No comments."
        feedback.add_course_feedback(course_id, rating, comments, user_id)

    def view_course_faq(self, user_id):
        content = course.list_course(4, user_id)
        if content is None:
            return
        course_name = get_string_input("Enter the name of course you wish to view FAQ of : ")
        is_valid_course_name, course_id = self.check_valid_course(course_name, content)
        if is_valid_course_name:
            faq.view_faq(course_name)

    def input_course_name_to_study_from(self, user_id):
        content = course.view_purchased_course(user_id)
        if content is None:
            return
        course_name = get_string_input("Enter the name of course you wish to study from : ")
        is_valid_course_name, course_id = self.check_valid_course(course_name, content)
        if is_valid_course_name:
            course_name = is_valid_course_name
            course.view_course_content(course_name)

    def check_pending_courses(self):
        query = get_query["PENDING_STATUS"]
        result = DatabaseConnection.get_from_db(query=query, val=("pending",))
        pending_course_count = 0
        if result:
            pending_course_count = result[0][0]

        return pending_course_count

    def list_pending_course(self, pending_course_count):
        print("**************************")
        print("Pending Notification : ")
        query = get_query.get("PENDING_STATUS")
        result = DatabaseConnection.get_from_db(query, ("pending",))

        print("Course details : \n")
        course_name = result[0][1]
        headers = ["Name", "Duration (in months)", "Price"]
        included_columns = [1, 3, 4]
        list_course_in_tabular_form(query, headers, "grid", included_columns, ("pending",))
        course.approve_course(course_name, pending_course_count)

    def input_course_faq(self, user_id):
        content = DatabaseConnection.get_from_db(get_query.get("GET_FAQ_DETAILS"), (user_id,))

        if len(content) == 0 or content is None:
            print("No course exists")
            return
        query = get_query.get("GET_FAQ_DETAILS")
        headers = ["Name", "Duration (in hrs )", "Price (in Rs.)", "Rating"]
        included_columns = [4, 6, 7, 8]
        list_course_in_tabular_form(query, headers, "grid", included_columns, user_id)
        course_name = get_string_input("Enter the name of the course in which you want to add FAQ : ")
        faq.add_faq(content, course_name)

    def input_purchase_course_name(self):
        try:
            user_input = input("Enter the name of course you wish to purchase : ")
            if user_input.strip() == '':
                print("Input cannot be empty. Please try again.")
                user_input = self.input_purchase_course_name()
            return user_input
        except:
            print("Wrong input made... please try again. ")
            return self.input_purchase_course_name()
