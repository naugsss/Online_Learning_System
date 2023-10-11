import os
from dotenv import load_dotenv
import hashlib
from datetime import date
import json
import logging
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
        except Exception as e:
            raise ValueError

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    with open(
        r"C:\\coding\WG\watchguard_daily_task_Aaryan\\online learning\\Online_Learning_System\src\\utils\\query_data.json",
        "r",
    ) as json_file:
        data = json.load(json_file)

    def insert_into_db(self, query, val=None):
        try:
            with DatabaseConnection() as db:
                cursor = db.cursor()
                if val is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, val)
                response = cursor.fetchall()
            return response
        except mysql.connector.Error as err:
            logging.error(err)

    def update_db(self, query, val=None):
        try:
            with DatabaseConnection() as db:
                cursor = db.cursor()
                if val is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, val)

        except mysql.connector.Error as err:
            logging.error(err)

    def delete_from_db(self, query, val=None):
        try:
            with DatabaseConnection() as db:
                cursor = db.cursor()
                if val is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, val)
        except mysql.connector.Error as err:
            logging.error(err)

    def get_from_db(self, query, val=None):
        try:
            with DatabaseConnection() as db:
                cursor = db.cursor()
                if val is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, val)
                response = cursor.fetchall()
            return response
        except mysql.connector.Error as err:
            logging.error(err)

    def get_role_from_db(self, query, val=None):
        try:
            with DatabaseConnection() as db:
                cursor = db.cursor()
                if val is None:
                    cursor.execute(query)
                    user_id = cursor.lastrowid
                    return user_id
                else:
                    cursor.execute(query, val)
                user_id = cursor.lastrowid
                return user_id
        except mysql.connector.Error as err:
            logging.error(err)

    def get_course_id(self, query, val=None):
        try:
            with DatabaseConnection() as db:
                cursor = db.cursor()
                if val is None:
                    cursor.execute(query)
                    course_id = cursor.lastrowid
                    return course_id
                else:
                    cursor.execute(query, val)
                course_id = cursor.lastrowid
                return course_id
        except mysql.connector.Error as err:
            logging.error(err)

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
