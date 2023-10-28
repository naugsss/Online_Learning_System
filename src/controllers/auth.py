import hashlib
from datetime import date
from src.configurations.config import sql_queries
from src.helpers.exceptions import LoginError
from src.models.database import db
from src.helpers.roles_enum import Roles

QUERIES = sql_queries


class Login:
    def __init__(self):
        self.role = 0
        self.user_id = any
        self.name = None
        self.username = None
        self.email = None
        self.password = None

    def login_user(self, username, password):
        """user logins with username and password

        Args:
            username (string): username of the user
            password (string): password of the user

        Returns:
            list: if credentials are valid, return role and user of the user else nothing.
        """
        self.username = username
        self.password = password
        user_data = self.validate_credentials(self.username, self.password)
        if user_data is not None:
            self.role = user_data[0]
            self.user_id = user_data[1]
            return [self.role, self.user_id]
        raise LoginError("Invalid Credentials")

    def sign_up(self, name, email, username, password):
        """user sign up with his details

        Args:
            name (string): name of the user
            email (string): email of the user
            username (string): username of the user
            password (string): password of the user

        Returns:
            list: if the details are valid, return the role and user id of the user else return None.
        """
        self.name = name
        self.email = email
        self.username = username
        self.password = password

        is_valid_username = db.get_from_db(
            QUERIES.get("GET_FROM_AUTHENTICATION"), (self.username,)
        )

        if is_valid_username:
            return None

        val = (name, email)
        self.user_id = db.insert_into_db(QUERIES.get("INSERT_USER_DETAILS"), val)

        val = (self.user_id, 4)
        db.insert_into_db(QUERIES.get("INSERT_USER_ROLES"), val)

        hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        val = (username, hashed_password, self.user_id, date.today())
        db.insert_into_db(QUERIES.get("INSERT_LOGIN_CREDENTIALS"), val)

        if self.user_id:
            user_data = self.login_user(username, password)
            if user_data is not None:
                return user_data
        

    def validate_credentials(self, username, password):
        """validate credentials against the given username and password

        Args:
            username (string): username of the user
            password (string): password of the user

        Returns:
            int: Role of the user, if valid otherwise returns None.
        """
        hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        response = db.get_from_db(QUERIES.get("GET_FROM_AUTHENTICATION"), (username,))
        if response is None or len(response) == 0:
            return None

        if response[0][2] == hashed_password:
            return self.get_role(response[0][3])

        return None

    def get_role(self, user_id):
        """get the role for the given user from the database

        Args:
            user_id (int): user id of the user

        Returns:
            list: role and user id of the user
        """
        result = db.get_from_db(QUERIES.get("GET_USER_ROLES"), (user_id,))
        role_id = result[0][2]
        return [role_id, user_id]

    @staticmethod
    def update_role(user_id):
        """update the role of the user

        Args:
            user_id (int): user id of the user.
        """
        result = db.get_from_db(QUERIES.get("GET_USER_ROLES"), (user_id,))
        for row in result:
            if row[2] == Roles.VISITOR.value:
                db.update_db(
                    QUERIES.get("UPDATE_USER_ROLES"), (Roles.STUDENT.value, user_id)
                )
                return
