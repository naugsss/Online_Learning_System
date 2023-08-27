from src.controllers.courses import Courses
from src.models.context_manager import DatabaseConnection


class Visitor(Courses):

    def calculate_earning(self):
        pass
    def delete_course(self):
        pass

    def approve_course(self):
        pass

    def list_course(self):
        try:
            with DatabaseConnection() as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM courses WHERE approval_status = %s and status = %s", ("approved", "active"))
                content = cursor.fetchall()
                keys = ["Name", "Duration", "Price", "Rating"]

                print("Courses available : \n")
                for row in content:
                    # print(row)
                    values = [row[1], row[3], row[4], row[5]]

                    result = dict(zip(keys, values))
                    for key, value in result.items():
                        print(key + ": ", value)
                    print("***************")
            return content
        except:
            print("There was some error in displaying course. Please try again.")

