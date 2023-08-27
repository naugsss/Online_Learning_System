from src.helpers.get_input import get_int_input, get_string_input
from src.models.databases import add_user_details, validate_user

LOGIN_VIEW = """
    ******** Welcome to Online Learning to System ********
    
    1. Sign Up
    2. Login
    3. Exit
"""


class Login:
    def __init__(self):
        self.role = 0
        self.user_id = any

    def login_user(self):
        username = get_string_input("Enter your username : ")
        password = get_string_input("Enter your password : ")
        user_data = validate_user(username, password)
        if user_data != None:
            self.role = user_data[0]
            self.user_id = user_data[1]
            return [self.role, self.user_id]

    def signup(self):
        user_name = get_string_input("Enter your name : ")
        user_email = get_string_input("Enter your email : ")
        username = get_string_input("Enter your username : ")
        password = get_string_input("Enter your password : ")
        self.user_id = add_user_details(user_name, user_email, username, password)
        if self.user_id:
            self.role, self.user_id = self.login_user()
            return [self.role, self.user_id]

    def login_menu(self):
        print(LOGIN_VIEW)
        user_input = get_int_input("Please enter your choice : ")

        while user_input != 3:
            if user_input == 1:
                self.signup()
                break
            elif user_input == 2:
                self.role, self.user_id = self.login_user()
                break
            else:
                print("Please enter correct choice.")
                print(LOGIN_VIEW)
                user_input = get_int_input("Please enter your choice : ")

        return [self.role, self.user_id]
