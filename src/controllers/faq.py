from tabulate import tabulate

from src.controllers.visitor import Visitor
from src.helpers.validators import get_string_input, get_int_input
from src.models.database import insert_into_db, get_from_db
from src.utils import queries


visitor = Visitor()

class Faq:

    def __init__(self):
        pass

    def view_faq(self):
        content = visitor.list_course()
        flag = 0
        user_input = get_string_input("Enter the name of the course of which you want to see FAQ : ")

        for row in content:
            if row[1].lower() == user_input.lower():
                flag = 1
                message = "There was some error"
                result = get_from_db(queries.GET_FAQ, (row[1],), message)
                if result is None or len(result) == 0:
                    print("No FAQ exists for this course.")
                else:
                    table = [(question, answer) for (_, _, _, _, _, _, _, _, _, _, _, _, _, question, answer, *_) in
                             result]
                    headers = ["Question", "Answer"]
                    table_str = tabulate(table, headers=headers, tablefmt="grid")
                    print(table_str)
        if flag == 0:
            print("No such course exists.")

    @staticmethod
    def add_faq(user_id):
        message = "There was some error while adding FAQ"
        content = insert_into_db(queries.GET_FAQ_DETAILS, (user_id,), message)
        print("Courses you've made : \n")

        table = [(name, duration, price, rating) for (_, _, _, _, name, _, duration, price, rating, *_) in content]
        headers = ["Name", "Duration (in months)", "Price", "Rating"]
        table_str = tabulate(table, headers=headers, tablefmt="grid")
        print(table_str)

        user_input = get_string_input("Enter the name of the course in which you want to add FAQ : ")
        for row in content:
            if row[4].lower() == user_input.lower():
                faq_count = get_int_input("How many FAQ you want to add (max 5 are allowed) : ")
                if faq_count > 5:
                    print("You can't add more than 5 FAQ's. Please enter a smaller number")
                    return
                else:
                    cnt = 0
                    while cnt < faq_count:
                        question = get_string_input("Enter the question : ")
                        answer = get_string_input("Enter it's answer : ")
                        insert_into_db(queries.INSERT_FAQ, (row[3], question, answer))
                        cnt += 1

                    print("**** FAQ added successfully ****")