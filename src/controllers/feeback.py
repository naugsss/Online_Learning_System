from datetime import date
from src.controllers.student import Student
from src.controllers.visitor import Visitor
from src.helpers.get_input import get_string_input, get_float_input, get_int_input
from src.models.context_manager import DatabaseConnection

student = Student()
visitor = Visitor()
class Feedback:

    def view_feedback(self):
        with DatabaseConnection() as db:
            cursor = db.cursor()
            content = student.list_course()
            user_input = get_string_input("Enter the name of course you wish to view feedback of : ")
            for row in content:
                if row[1].lower() == user_input.lower():
                    cursor.execute("SELECT * FROM course_feedback WHERE cid = %s", (row[0],))
                    result = cursor.fetchall()
                    if len(result) != 0:
                        for value in result:
                            print("Rating : ", value[3])
                            print("Comment : ", value[4])
                            print("************")
                    else:
                        print("No feedback exists for this course.")

    def add_feedback(self, user_id):
        # try:
        with DatabaseConnection() as db:
            try:
                cursor = db.cursor()
                content = student.view_purchased_course(user_id)

                user_input = get_string_input("Enter the name of course you wish to add feedback to : ")
                for row in content:
                    if row[1].lower() == user_input.lower():

                        print("**** Add feedback ****")
                        rating = get_float_input("Enter rating out of 5 : ")
                        comments = get_string_input("Enter any comment : ")
                        sql = "INSERT INTO course_feedback (cid, uid, rating, comments, created_at) VALUES (%s, %s, %s, %s, %s)"
                        val = (row[0], user_id, rating, comments, date.today())
                        cursor.execute(sql, val)

                        cursor.execute("SELECT AVG(rating) FROM course_feedback where cid = %s", (row[0],))
                        ratings = cursor.fetchone()
                        ratings = round(ratings[0], 2)
                        cursor.execute("UPDATE courses SET avg_rating = %s WHERE id = %s", (ratings, row[0]))
                        print("Feedback added successfully.")
            except:
                print("There was some issue while adding feedback, please try again..")

    def view_faq(self):
        with DatabaseConnection() as db:
            cursor = db.cursor()
            content = visitor.list_course()
            user_input = get_string_input("Enter the name of the course of which you want to see FAQ : ")
            for row in content:
                if row[1].lower() == user_input.lower():
                    cursor.execute("SELECT * FROM courses, course_faq WHERE name = %s AND courses.id = course_faq.cid ", (row[1],))
                    result = cursor.fetchall()
                    keys = ["Question", "Answer"]
                    for item in result:
                        values = [item[13], item[14]]

                        result = dict(zip(keys, values))
                        for key, value in result.items():
                            print(key + ": ", value)
                        print("***************")

    def add_faq(self, user_id):
        with DatabaseConnection() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM mentor_course, courses WHERE uid = %s and mentor_course.cid = courses.id", (user_id,))
            content = cursor.fetchall()
            keys = ["Name", "Duration", "Price", "Rating"]

            print("Courses you've made : \n")
            for row in content:
                print(row)
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
                            cursor.execute("INSERT INTO course_faq (cid, question, answer) VALUES (%s, %s, %s)", (row[3], question, answer))
                            cnt += 1

                        print("**** FAQ added successfully ****")

