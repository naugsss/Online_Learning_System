from src.controllers.admin import Admin
from src.helpers.login import Login
from src.utils.menu_prompt_functions import prompt_admin_menu, prompt_student_menu, prompt_mentor_menu, \
    prompt_visitor_menu

if __name__ == '__main__':
    login = Login()
    role, user_id = login.login_menu()

    if role == 1:
        admin = Admin()
        admin.approve_course()
        prompt_admin_menu(user_id)
    elif role == 2:
        # student
        prompt_student_menu(user_id)
    elif role == 3:
        # mentor
        prompt_mentor_menu(user_id)
    elif role == 4:
        # visitor
        prompt_visitor_menu(user_id)

