import mysql.connector
from dotenv import load_dotenv
import logging
import json

load_dotenv()


class DatabaseConnection:

    def __init__(self):

        self.db = mysql.connector.connect(
            host="localhost",
            user="naugs",
            password="ashupatna123##",
            database="lms",
            autocommit=True
        )

        self.cursor = self.db.cursor()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    with open('C:\coding\WG\watchguard_daily_task_Aaryan\Online-Learning-System-Project - Copy with tests\src\\utils\query_data.json', 'r') as json_file:
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
            print("Please check you inputs and try once again.")

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
            print("Please check you inputs and try once again.")

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
            print("Please check you inputs and try once again.")

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
            print("Please check you inputs and try once again.")

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
            print("Please check you inputs and try once again.")

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
            print("Please check you inputs and try once again.")
