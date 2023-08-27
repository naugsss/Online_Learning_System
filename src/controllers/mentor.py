from src.controllers.courses import Courses
from src.helpers.get_input import get_string_input
from src.models.context_manager import DatabaseConnection


class Mentor(Courses):
    def calculate_earning(self, user_id):
        try:
            with DatabaseConnection() as db:
                cursor = db.cursor()
                cursor.execute(
                    "SELECT price, no_of_students, name FROM courses, mentor_course WHERE courses.id = mentor_course.cid AND uid = %s", (user_id,))
                result = cursor.fetchall()
                for row in result:
                    cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
                    name = cursor.fetchall()
                    print("****************************")
                    print("Mentor name : ", name[0][0])
                    print("Course name : ", row[2])
                    print("Earnings : ", row[0] * row[1])
        except:
            print("There was an error in displaying the earnings..")

    def delete_course(self):
        pass

    def add_mentor(self):
        user_name = get_string_input("Enter the username of the user whom you wish to make admin : ")
        try:
            with DatabaseConnection() as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM authentication WHERE username = %s", (user_name,))
                result = cursor.fetchone()
                print(result)
                sql = "INSERT INTO user_roles (uid, role_id) VALUES (%s, %s)"
                val = (result[3], 3)
                cursor.execute(sql, val)
                print("**** Mentor added successfully ****")
        except:
            print("Couldn't add mentor, please try again ...")

    def list_course(self):
        with DatabaseConnection() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM courses WHERE approval_status = %s", ("approved",))
            content = cursor.fetchall()
            keys = ["Name", "Duration", "Price", "Rating", "Status"]

            print("Courses available : \n")
            for row in content:
                # print(row)
                values = [row[1], row[3], row[4], row[5], row[8]]

                result = dict(zip(keys, values))
                for key, value in result.items():
                    print(key + ": ", value)
                print("***************")
