from abc import abstractmethod, ABC
from src.helpers.config import get_pending_course_count, update_pending_course_count
from src.helpers.get_input import get_string_input, get_int_input
from datetime import date
from src.models.context_manager import DatabaseConnection


class Courses(ABC):

    def __init__(self):
        pass

    def add_course(self, user_id):
        course_name = get_string_input("Enter name of course : ")
        content = get_string_input("Enter content of course : ")
        duration = get_int_input("Enter duration of course in months : ")
        price = get_int_input("Enter price of course : ")
        pending_course_count = get_pending_course_count()
        try:
            with DatabaseConnection() as db:
                cursor = db.cursor()
                sql = "INSERT INTO courses (name, content, duration, price, avg_rating, approval_status, no_of_students, status, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (course_name, content, duration, price, 0, "pending", 0, "active", date.today(), date.today())
                cursor.execute(sql, val)
                course_id = cursor.lastrowid
                cursor.execute("INSERT INTO mentor_course (cid, uid) VALUES (%s, %s)", (course_id, user_id))
                pending_course_count += 1
                print("**** Course added successfully ****")
                update_pending_course_count(pending_course_count)
        except:
            print("There was an error in adding course.. Please try again")

    @abstractmethod
    def list_course(self):
        print("This is an abstract method.")

    @abstractmethod
    def delete_course(self):
        pass

    @abstractmethod
    def calculate_earning(self, user_id):
        pass

    # @abstractmethod
    def approve_course(self):
        pass

    def view_purchased_course(self, user_id):
        try:
            with DatabaseConnection() as db:
                cursor = db.cursor()
                cursor.execute(
                    "SELECT * FROM courses, student_course WHERE uid = %s and student_course.cid = courses.id",
                    (user_id,))
                content = cursor.fetchall()
                keys = ["Name", "Duration", "Price", "Rating"]

                print("Courses you've purchased : \n")
                for row in content:
                    values = [row[1], row[3], row[4], row[5]]

                    result = dict(zip(keys, values))
                    for key, value in result.items():
                        print(key + ": ", value)
                    print("***************")

            return content
        except:
            print("There was an error in fetching the content. Please try again..")

    def view_course_content(self, user_id):
        try:
            with DatabaseConnection() as db:
                cursor = db.cursor()
                content = self.view_purchased_course(user_id)

                user_input = get_string_input("Enter the name of course you wish to study from : ")
                for row in content:
                    if row[1].lower() == user_input.lower():
                        print(row[1])
                        cursor.execute("SELECT * FROM courses WHERE name = %s", (row[1],))
                        result = cursor.fetchone()
                        print("**** Content Begins **** ")
                        print(result[2])
                        print("**** END **** ")


        except:
            print("There was an error in fetching the content. Please try again..")

    def purchase_course(self, user_id):
        try:
            with DatabaseConnection() as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM courses WHERE approval_status = %s and status = %s",
                               ("approved", "active"))
                content = cursor.fetchall()
                keys = ["Name", "Duration", "Price", "Rating"]

                print("Courses available : \n")
                for row in content:
                    values = [row[1], row[3], row[4], row[5]]

                    result = dict(zip(keys, values))
                    for key, value in result.items():
                        print(key + ": ", value)
                    print("***************")
                user_input = get_string_input("Enter the name of course you wish to purchase : ")

                for row in content:
                    if row[1].lower() == user_input.lower():
                        cursor.execute("SELECT * FROM student_course where uid = %s and cid = %s", (user_id, row[0]))
                        result = cursor.fetchone()
                        if result is None:
                            cursor.execute("INSERT INTO student_course (uid, cid, purchased_on) VALUES (%s, %s, %s)",
                                           (user_id, row[0], date.today()))
                            cursor.execute("SELECT no_of_students from courses where id = %s", (row[0],))

                            no_of_students = cursor.fetchone()
                            updated_no_of_student = no_of_students[0]
                            updated_no_of_student += 1
                            cursor.execute("UPDATE courses SET no_of_students = %s where id = %s",
                                           (updated_no_of_student, row[0]))
                            print("**** Course purchased successfully ****")

                        else:
                            print("You've already purchased this course.")
                cursor.execute("SELECT * FROM user_roles where uid = %s", (user_id,))
                result = cursor.fetchall()
                for row in result:
                    if row[2] == 4:
                        cursor.execute("UPDATE user_roles SET role_id = %s WHERE uid = %s", (2, user_id))
                        return
        except:
            print("There was some error, please try again..")
