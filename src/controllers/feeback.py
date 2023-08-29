from datetime import date
from tabulate import tabulate
from src.controllers.student import Student
from src.controllers.visitor import Visitor
from src.helpers.validators import get_string_input, get_float_input, get_int_input
from src.models.database import get_from_db, insert_into_db, update_db
from src.utils import queries

student = Student()
visitor = Visitor()


class Feedback:

    @staticmethod
    def view_feedback():
        content = student.list_course()
        user_input = get_string_input("Enter the name of course you wish to view feedback of : ")
        flag = 0
        for row in content:
            if row[1].lower() == user_input.lower():
                flag = 1
                val = (row[0],)
                message = "There was error in displaying feedback."
                result = get_from_db(queries.GET_FROM_COURSE_FEEDBACK, val, message)

                if len(result) != 0:
                    table = [(rating, comment) for (_, _, _, rating, comment, *_) in result]
                    headers = ["Rating", "Comment"]
                    table_str = tabulate(table, headers=headers, tablefmt="grid")
                    print(table_str)
                else:
                    print("No feedback exists for this course.")
        if flag == 0:
            print("No such course exists.")

    @staticmethod
    def add_feedback(user_id):
        content = student.view_purchased_course(user_id)
        user_input = get_string_input("Enter the name of course you wish to add feedback to : ")
        flag = 0
        for row in content:
            if row[1].lower() == user_input.lower():
                flag = 1
                print("**** Add feedback ****")
                rating = get_float_input("Enter rating out of 5 : ")
                while rating > 5 or rating <= 0:
                    rating = get_float_input("Enter rating out of 5 : ")
                    if 5 > rating > 0:
                        break
                comments = get_string_input("Enter any comment : ")
                if comments == "":
                    comments = "No comments."
                val = (row[0], user_id, rating, comments, date.today())
                message = "feedback was not added."
                insert_into_db(queries.INSERT_INTO_COURSE_FEEDBACK, val, message)

                message = "There was some error. Please try again"
                ratings = get_from_db(queries.GET_AVG_RATING_COURSE_FEEDBACK, (row[0],), message)
                ratings = round(ratings[0][0], 2)

                message = "There was error in updating the course."
                update_db(queries.UPDATE_AVG_RATING, (ratings, row[0]), message)
                print("**** Feedback added successfully ****")
        if flag == 0:
            print("No such course exists.")

    @staticmethod
    def view_faq():
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

