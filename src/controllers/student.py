from src.controllers.courses import Courses
from src.models.context_manager import DatabaseConnection


class Student(Courses):

    def calculate_earning(self):
        pass

    def delete_course(self):
        pass

    def list_course(self):
        with DatabaseConnection() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM courses WHERE approval_status = %s and status = %s", ("approved", "active"))
            content = cursor.fetchall()
            keys = ["Name", "Duration", "Price", "Rating"]

            print("Courses available : \n")
            for row in content:

                values = [row[1], row[3], row[4], row[5]]

                result = dict(zip(keys, values))
                for key, value in result.items():
                    print(key + ": ", value)
                print("***************")
            return content

    def approve_course(self):
        pass


    def view_student_details(self):
        with DatabaseConnection() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM student_course")
            result = cursor.fetchall()
            print("Here are the details of the user:")

            for row in result:
                cursor.execute("SELECT name FROM users WHERE id = %s", (row[1],))
                user_name = cursor.fetchone()
                cursor.execute("SELECT name FROM courses WHERE id = %s", (row[2],))
                course_name = cursor.fetchall()
                print("********************")
                print("Name : ", user_name[0])
                print("Course purchased : ", course_name[0][0])



