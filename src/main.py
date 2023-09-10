import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.controllers.courses import Courses
from src.controllers.auth import Login
from src.helpers.entry_menu import EntryMenu

loginview = EntryMenu()

course = Courses()
if __name__ == '__main__':
    login = Login()
    role, user_id = login.login_menu()

    if role == 1:
        EntryMenu.prompt_admin_menu(loginview, role, user_id)
    elif role == 2:
        # student
        EntryMenu.prompt_student_menu(loginview, role, user_id)
    elif role == 3:
        # mentor
        EntryMenu.prompt_mentor_menu(loginview, role, user_id)
    elif role == 4:
        # visitor
        EntryMenu.prompt_visitor_menu(loginview, role, user_id)
