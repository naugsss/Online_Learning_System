from src.controllers.courses import Courses
from src.models.auth import Login
from src.utils.menu_prompt_functions import prompt_admin_menu, prompt_student_menu, prompt_mentor_menu, \
    prompt_visitor_menu
course = Courses()
if __name__ == '__main__':
    login = Login()
    role, user_id = login.login_menu()

    if role == 1:
        course.approve_course()
        prompt_admin_menu(role, user_id)
    elif role == 2:
        # student
        prompt_student_menu(role, user_id)
    elif role == 3:
        # mentor
        prompt_mentor_menu(role, user_id)
    elif role == 4:
        # visitor
        prompt_visitor_menu(role, user_id)
