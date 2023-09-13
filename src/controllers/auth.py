import hashlib
import re
import maskpass

from src.helpers.inputs_and_validations import validate_email, validate_password, \
    input_name, input_email, input_user_name
from src.models.fetch_json_data import JsonData
from src.models.database import DatabaseConnection

get_query = JsonData.load_data()
LOGIN_VIEW = """
    ******** Welcome to Online Learning System ********
    
    1. Sign Up
    2. Login
    3. Exit
"""

DatabaseConnection = DatabaseConnection()


class Login:
    def __init__(self):
        self.role = 0
        self.user_id = any
        self.name = None
        self.username = None
        self.email = None
        self.password = None

    def login_user(self):
        input_user_name(self)
        self.password = maskpass.askpass(prompt="Enter your password : ", mask="*")
        user_data = self.validate_user(self.username, self.password)
        if user_data != None:
            self.role = user_data[0]
            self.user_id = user_data[1]
            return [self.role, self.user_id]

    def sign_up(self):
        input_name(self)
        input_email(self)
        if validate_email(self.email):
            input_user_name(self)
            is_valid_username = DatabaseConnection.get_from_db(get_query.get("GET_FROM_AUTHENTICATION"), (self.username,))
            if is_valid_username:
                print("This username already exists. Please try with different username.")
                return
            self.password = maskpass.askpass(prompt="Enter your password : ", mask="*")
            if validate_password(self.password):
                self.user_id = DatabaseConnection.insert_user_details(self.name, self.email, self.username,
                                                                      self.password)
                if self.user_id:
                    user_data = self.login_user()
                    if user_data is not None:
                        self.role = user_data[0]
                        self.user_id = user_data[1]
                        return [self.role, self.user_id]

    def login_menu(self):
        print(LOGIN_VIEW)
        user_input = input_choice()

        while user_input != 3:
            if user_input == 1:
                self.sign_up()
                break
            elif user_input == 2:
                user_details = self.login_user()
                if user_details is not None:
                    self.role, self.user_id = user_details
                break
            else:
                print("Please enter correct choice.")
                print(LOGIN_VIEW)
                user_input = input_choice()

        return [self.role, self.user_id]

    def validate_user(self, username, password):
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        response = DatabaseConnection.get_from_db(get_query.get("GET_FROM_AUTHENTICATION"), (username,))

        if response is None or len(response) == 0:
            print("No such user exists.")
        else:
            if response[0][2] == hashed_password:
                print("You logged into the system successfully.")
                return self.get_role(response[0][3])
            else:
                print("You entered wrong password. ")

    def get_role(self, user_id):
        result = DatabaseConnection.get_from_db(get_query.get("GET_USER_ROLES"), (user_id,))
        role_id = result[0][2]
        return [role_id, user_id]

    @staticmethod
    def update_role(user_id):
        result = DatabaseConnection.get_from_db(get_query.get("GET_USER_ROLES"), (user_id,))
        for row in result:
            if row[2] == 4:
                DatabaseConnection.update_db(get_query.get("UPDATE_USER_ROLES"), (2, user_id))
                return

    # def input_user_name(self):
    #     self.username = input("Enter your username : ")
    #     is_valid_username = validate_username(self.username)
    #     if is_valid_username is None:
    #         print("Enter a valid username...")
    #         self.input_user_name()

    # def input_email(self):
    #     self.email = input("Enter your email : ")
    #     is_valid_email = validate_email(self.email)
    #     if is_valid_email is None:
    #         self.input_email()


def input_choice():
    pattern = '[1-9]+'
    user_input = input("Please enter your choice : ")
    if re.fullmatch(pattern, user_input):
        return int(user_input)
    else:
        print("Please enter valid number...")
        return input_choice()
