from tabulate import tabulate
from src.controllers.courses import Courses
from src.helpers.inputs_and_validations import get_string_input
from src.models.database import DatabaseConnection
from src.utils import queries


DatabaseConnection = DatabaseConnection()
course = Courses()

class Faq:

    def __init__(self):
        pass

    def view_faq(self, user_id):
        content = course.list_course(4, user_id)
        is_valid_input = False
        user_input = get_string_input("Enter the name of the course of which you want to see FAQ : ")

        for row in content:
            if row[1].lower() == user_input.lower():
                is_valid_input = True
                result = DatabaseConnection.get_from_db(queries.GET_FAQ, (row[1],))
                if result is None or len(result) == 0:
                    print("No FAQ exists for this course.")
                else:
                    table = [(question, answer) for (_, _, _, _, _, _, _, _, _, _, _, _, _, question, answer, *_) in
                             result]
                    headers = ["Question", "Answer"]
                    table_str = tabulate(table, headers=headers, tablefmt="grid")
                    print(table_str)
        if not is_valid_input:
            print("No such course exists.")

    def add_faq(self, user_id):
        content = DatabaseConnection.insert_into_db(queries.GET_FAQ_DETAILS, (user_id,))
        print("Courses you've made : \n")

        table = [(name, duration, price, rating) for (_, _, _, _, name, _, duration, price, rating, *_) in content]
        headers = ["Name", "Duration (in hrs )", "Price (in Rs.)", "Rating"]
        table_str = tabulate(table, headers=headers, tablefmt="grid")
        print(table_str)

        user_input = get_string_input("Enter the name of the course in which you want to add FAQ : ")
        for row in content:
            if row[4].lower() == user_input.lower():
                faq_count = input_faq_count()

                cnt = 0
                while cnt < faq_count:
                    question = get_string_input("Enter the question : ")
                    answer = get_string_input("Enter it's answer : ")
                    DatabaseConnection.insert_into_db(queries.INSERT_FAQ, (row[3], question, answer))
                    cnt += 1

                print("**** FAQ added successfully ****")


def input_faq_count():
    user_input = int(input("How many FAQ you want to add (max 5 are allowed) : "))
    if user_input <= 0:
        print("input cannot be less than 0.. please try again. ")
        return input_faq_count()
    elif user_input > 0 and user_input < 5:
        return user_input
    elif user_input > 5:
        print("Enter a value less than equal to 5")
        return input_faq_count()
    else:
        print("Please enter price of course (in Rs.) : ")
        return input_faq_count()