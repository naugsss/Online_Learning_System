# from tabulate import tabulate
# from src.controllers.courses import Courses
# from src.models.database import DatabaseConnection
# from src.models.fetch_json_data import JsonData

# DatabaseConnection = DatabaseConnection()
# get_query = JsonData.load_data()


# class Student(Courses):

#     def view_student_details(self):
#         result = DatabaseConnection.get_from_db(get_query.get("GET_USER_DETAILS"))
#         print("Here are the details of the user:")
#         values = []
#         for row in result:
#             user_name = DatabaseConnection.get_from_db(get_query.get("GET_NAME"), (row[1],))
#             course_name = DatabaseConnection.get_from_db(get_query.get("GET_COURSE_NAME"), (row[2],))
#             values.append([user_name[0][0], course_name[0][0]])

#         print(tabulate(values, headers=['Name', 'Course Purchased'], tablefmt="grid"))

