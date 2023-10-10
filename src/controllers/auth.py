import hashlib
from helpers.inputs_and_validations import validate_email, validate_password
from models.fetch_json_data import JsonData
from models.database import db
from helpers.roles_enum import Roles

get_query = JsonData.load_data()


class Login:
    def __init__(self):
        self.role = 0
        self.user_id = any
        self.name = None
        self.username = None
        self.email = None
        self.password = None

    def login_user(self, username, password):
        self.username = username
        self.password = password
        user_data = self.validate_credentials(self.username, self.password)
        if user_data is not None:
            self.role = user_data[0]
            self.user_id = user_data[1]
            return [self.role, self.user_id]
        return None

    def sign_up(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        if validate_email(self.email):
            is_valid_username = db.get_from_db(
                get_query.get("GET_FROM_AUTHENTICATION"), (self.username,)
            )
            if is_valid_username:
                return None
            # iss cheez ko json schema mein check krna h
            if validate_password(self.password):
                self.user_id = db.insert_user_details(
                    self.name, self.email, self.username, self.password
                )
                if self.user_id:
                    user_data = self.login_user(username, password)
                    if user_data is not None:
                        self.role = user_data[0]
                        self.user_id = user_data[1]
                        return [self.role, self.user_id]
            else:
                return "Invalid password"
        else:
            return "Invalid email id"

    def validate_credentials(self, username, password):
        hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        response = db.get_from_db(get_query.get("GET_FROM_AUTHENTICATION"), (username,))

        if response is None or len(response) == 0:
            return None
        else:
            if response[0][2] == hashed_password:
                return self.get_role(response[0][3])
            else:
                return None

    def get_role(self, user_id):
        result = db.get_from_db(get_query.get("GET_USER_ROLES"), (user_id,))
        role_id = result[0][2]
        return [role_id, user_id]

    @staticmethod
    def update_role(user_id):
        result = db.get_from_db(get_query.get("GET_USER_ROLES"), (user_id,))
        for row in result:
            if row[2] == Roles.VISITOR.value:
                db.update_db(
                    get_query.get("UPDATE_USER_ROLES"), (Roles.STUDENT.value, user_id)
                )
                return
