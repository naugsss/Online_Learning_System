from src.controllers.courses import Courses
from src.controllers.student import Student
from src.helpers.config import update_pending_course_count, get_pending_course_count
from src.helpers.get_input import get_string_input
from src.models.context_manager import DatabaseConnection


class Admin(Courses):

    def calculate_earning(self):
        try:
            with DatabaseConnection() as db:
                cursor = db.cursor()
                cursor.execute(
                    "SELECT price, no_of_students, name, uid FROM courses, mentor_course WHERE courses.id = mentor_course.cid ")
                result = cursor.fetchall()
                for row in result:
                    # print(row)
                    cursor.execute("SELECT name FROM users WHERE id = %s", (row[3],))
                    name = cursor.fetchall()
                    # print(name)
                    print("****************************")
                    print("Mentor name : ", name[0][0])
                    print("Course name : ", row[2])
                    print("Earnings : ", row[0] * row[1])
        except:
            print("There was an error in displaying the earnings..")

    def approve_course(self):
        pending_course_count = get_pending_course_count()

        if pending_course_count > 0:

            try:

                with DatabaseConnection() as db:
                    cursor = db.cursor()

                    cursor.execute("SELECT * FROM courses WHERE approval_status = %s", ("pending",))
                    result = cursor.fetchall()
                    keys = ["Name", "Duration", "Price"]

                    print("Course details : \n")
                    for row in result:

                        values = [row[1], row[3], row[4]]

                        result = dict(zip(keys, values))
                        for key, value in result.items():
                            print(key + ": ", value)
                        print("***************")

                        admin_input = get_string_input("Do you want to approve or reject this course : ")
                        if admin_input == "approve":
                            cursor.execute("UPDATE courses SET approval_status = %s WHERE id = %s",
                                           ("approved", row[0]))
                            print("**** Course approved successfully ****")
                        else:
                            cursor.execute("DELETE FROM mentor_course WHERE cid = %s", (row[0],))
                            cursor.execute("DELETE FROM courses WHERE id = %s", (row[0],))
                            print("**** Course rejected ****")
                pending_course_count -= 1
                update_pending_course_count(0)
            except:
                print("There was some error in displaying courses for approval.")

    def delete_course(self):
        try:
            with DatabaseConnection() as db:
                cursor = db.cursor()
                student = Student()
                content = student.list_course()
                user_input = get_string_input("Enter the name of the course you wish to delete : ")
                for row in content:
                    if row[1].lower() == user_input.lower():
                        cursor.execute("UPDATE courses SET status = %s WHERE name = %s", ("deactive", row[1]))
                        print("**** Course marked as deactive successfully ****")
                        break

        except:
            pass

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
