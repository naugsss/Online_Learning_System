import os
import hashlib
from datetime import date
from dotenv import load_dotenv
import mysql.connector

load_dotenv()


class DatabaseConnection:
    def __init__(self):
        try:
            self.db = mysql.connector.connect(
                host=os.getenv("HOST"),
                user=os.getenv("USER"),
                password=os.getenv("PASSWORD"),
                database=os.getenv("DATABASE"),
                autocommit=True,
            )

            self.cursor = self.db.cursor()
        except Exception:
            raise ValueError

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def insert_into_db(self, query, val=None):
        if val is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, val)
        response = self.cursor.fetchall()
        return response

    def update_db(self, query, val=None):
        if val is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, val)

    def delete_from_db(self, query, val=None):
        if val is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, val)

    def get_from_db(self, query, val=None):
        if val is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, val)
        response = self.cursor.fetchall()
        return response

    def get_role_from_db(self, query, val=None):
        if val is None:
            self.cursor.execute(query)
            user_id = self.cursor.lastrowid
            return user_id

        self.cursor.execute(query, val)
        user_id = self.cursor.lastrowid
        return user_id

    def get_course_id(self, query, val=None):
        """get the course id from the database"""

        if val is None:
            self.cursor.execute(query)
            course_id = self.cursor.lastrowid
            return course_id
        else:
            self.cursor.execute(query, val)
        course_id = self.cursor.lastrowid
        return course_id

    def insert_user_details(self, name, email, username, password):
        sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
        val = (name, email)
        user_id = self.get_role_from_db(sql, val)
        sql = "INSERT INTO user_roles (uid, role_id) VALUES (%s, %s)"
        val = (user_id, 4)
        self.insert_into_db(sql, val)

        hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        sql = "INSERT INTO authentication (username, password, uid, create_at) VALUES (%s, %s, %s, %s)"
        val = (username, hashed_password, user_id, date.today())
        self.insert_into_db(sql, val)
        return user_id


try:
    db = DatabaseConnection()
except:
    raise ValueError
