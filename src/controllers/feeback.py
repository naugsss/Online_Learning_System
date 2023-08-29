from datetime import date
from tabulate import tabulate
from src.controllers.courses import Courses
from src.helpers.inputs_and_validations import get_string_input, get_float_input
from src.models.database import DatabaseConnection
from src.utils import queries

course = Courses()
DatabaseConnection = DatabaseConnection()


class Feedback:

    def view_feedback(self, role):
        content = course.list_course(2, role)
        user_input = get_string_input("Enter the name of course you wish to view feedback of : ")
        is_valid_input = False
        for row in content:
            if row[1].lower() == user_input.lower():
                is_valid_input = True
                val = (row[0],)
                result = DatabaseConnection.get_from_db(queries.GET_FROM_COURSE_FEEDBACK, val)

                if len(result) != 0:
                    table = [(rating, comment) for (_, _, _, rating, comment, *_) in result]
                    headers = ["Rating", "Comment"]
                    table_str = tabulate(table, headers=headers, tablefmt="grid")
                    print(table_str)
                else:
                    print("No feedback exists for this course.")
        if not is_valid_input:
            print("No such course exists.")


    def add_feedback(self, user_id):
        content = course.view_purchased_course(user_id)
        user_input = get_string_input("Enter the name of course you wish to add feedback to : ")
        is_valid_input = False
        for row in content:
            if row[1].lower() == user_input.lower():
                is_valid_input = True
                print("**** Add feedback ****")
                rating = float(input("Enter rating out of 5 : "))
                while rating > 5 or rating <= 0:
                    rating = get_float_input("Enter rating out of 5 : ")
                    if rating > 0 and rating < 5:
                        break
                comments = input("Enter any comment : ")
                if comments == "":
                    comments = "No comments."
                val = (row[0], user_id, rating, comments, date.today())
                DatabaseConnection.insert_into_db(queries.INSERT_INTO_COURSE_FEEDBACK, val)

                ratings = DatabaseConnection.get_from_db(queries.GET_AVG_RATING_COURSE_FEEDBACK, (row[0],))
                ratings = round(ratings[0][0], 2)

                DatabaseConnection.update_db(queries.UPDATE_AVG_RATING, (ratings, row[0]))
                print("**** Feedback added successfully ****")
        if not is_valid_input:
            print("No such course exists.")
