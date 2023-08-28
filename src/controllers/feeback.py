from datetime import date
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
                    for value in result:
                        print("Rating : ", value[3])
                        print("Comment : ", value[4])
                        print("************")
                else:
                    print("No feedback exists for this course.")
        if flag == 0:
            print("No such course exists.")

    @staticmethod
    def add_feedback(user_id):
        content = student.view_purchased_course(user_id)
        user_input = get_string_input("Enter the name of course you wish to add feedback to : ")
        for row in content:
            if row[1].lower() == user_input.lower():
                print("**** Add feedback ****")
                rating = get_float_input("Enter rating out of 5 : ")
                comments = get_string_input("Enter any comment : ")
                val = (row[0], user_id, rating, comments, date.today())
                message = "feedback was not added."
                insert_into_db(queries.INSERT_INTO_COURSE_FEEDBACK, val, message)

                message = "There was some error. Please try again"
                ratings = get_from_db(queries.GET_AVG_RATING_COURSE_FEEDBACK, (row[0],), message)
                ratings = round(ratings[0][0], 2)

                message = "There was error in updating the course."
                update_db(queries.UPDATE_AVG_RATING, (ratings, row[0]), message)
                print("**** Feedback added successfully ****")

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
                keys = ["Question", "Answer"]
                if result is None or len(result) == 0:
                    print("No FAQ exists for this course.")
                else:
                    for item in result:
                        values = [item[13], item[14]]
                        result = dict(zip(keys, values))
                        for key, value in result.items():
                            print(key + ": ", value)
                        print("***************")
        if flag == 0:
            print("No such course exists.")

    @staticmethod
    def add_faq(user_id):
        message = "There was some error while adding FAQ"
        content = insert_into_db(queries.GET_FAQ_DETAILS, (user_id,), message)
        keys = ["Name", "Duration", "Price", "Rating"]

        print("Courses you've made : \n")
        for row in content:
            values = [row[4], row[6], row[7], row[8]]

            result = dict(zip(keys, values))
            for key, value in result.items():
                print(key + ": ", value)
            print("***************")

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
