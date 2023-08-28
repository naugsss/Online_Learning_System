import hashlib
from datetime import date
from src.helpers.validators import get_int_input, get_string_input, validate_email, validate_password
import maskpass
from src.models.context_manager import DatabaseConnection
from src.models.database import get_from_db
from src.utils import queries

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
        self.name = None
        self.username = None
        self.email = None
        self.password = None

    def login_user(self):
        self.username = get_string_input("Enter your username : ")
        self.password = maskpass.askpass(prompt="Enter your password : ", mask="*")
        user_data = self.validate_user(self.username, self.password)
        if user_data != None:
            self.role = user_data[0]
            self.user_id = user_data[1]
            return [self.role, self.user_id]

    def signup(self):
        self.name = get_string_input("Enter your name : ")
        self.email = get_string_input("Enter your email : ")
        if validate_email(self.email):
            self.username = get_string_input("Enter your username : ")
            self.password = maskpass.askpass(prompt="Enter your password : ", mask="*")
            if validate_password(self.password):
                self.user_id = self.add_user_details(self.name, self.email, self.username, self.password)
                if self.user_id:
                    user_data = self.login_user()
                    if user_data is not None:
                        self.role = user_data[0]
                        self.user_id = user_data[1]
                        return [self.role, self.user_id]

    def login_menu(self):
        print(LOGIN_VIEW)
        user_input = get_int_input("Please enter your choice : ")

        while user_input != 3:
            if user_input == 1:
                self.signup()
                break
            elif user_input == 2:
                user_details = self.login_user()
                if user_details is not None:
                    self.role, self.user_id = user_details
                break
            else:
                print("Please enter correct choice.")
                print(LOGIN_VIEW)
                user_input = get_int_input("Please enter your choice : ")

        return [self.role, self.user_id]

    @staticmethod
    def add_user_details(name, email, username, password):
        try:
            with DatabaseConnection() as db:
                cursor = db.cursor()
                sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
                val = (name, email)
                cursor.execute(sql, val)
                user_id = cursor.lastrowid

                sql = "INSERT INTO user_roles (uid, role_id) VALUES (%s, %s)"
                val = (user_id, 4)
                cursor.execute(sql, val)

                hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                sql = "INSERT INTO authentication (username, password, uid, create_at) VALUES (%s, %s, %s, %s)"
                val = (username, hashed_password, user_id, date.today())
                cursor.execute(sql, val)

                print("**** Account created successfully ****")
                return user_id
        except:
            print("An error occurred while inserting into database. Please try again..")
            return False

    def validate_user(self, username, password):
        # adding data to authentication table
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        message = "Error occurred while inserting data"
        response = get_from_db(queries.GET_FROM_AUTHENTICATION, (username,), message)

        if response is None or len(response) == 0:
            print("No such user exists.")
        else:
            if response[0][2] == hashed_password:
                print("You logged into the system successfully.")
                return self.get_role(response[0][3])
            else:
                print("You entered wrong password. ")

    @staticmethod
    def get_role(user_id):

        message = "Couldn't fetch a role."
        result = get_from_db(queries.GET_USER_ROLES, (user_id,), message)
        role_id = result[0][2]
        return [role_id, user_id]
