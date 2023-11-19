import os
from dotenv import load_dotenv
import mysql.connector

from src.helpers.exceptions import DbException

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

    def insert_into_db(self, query, val):
        try:
            self.cursor.execute(query, val)
            user_id = self.cursor.lastrowid
            return user_id
        except:
            raise DbException

    def update_db(self, query, val):
        try:
            self.cursor.execute(query, val)
            return self.cursor.lastrowid
        except:
            raise DbException

    def delete_from_db(self, query, val):
        try:
            self.cursor.execute(query, val)
        except:
            raise DbException

    def get_from_db(self, query, val=None):
        try:
            if val is None:
                self.cursor.execute(query)
                response = self.cursor.fetchall()
                return response
            else:
                self.cursor.execute(query, val)
            response = self.cursor.fetchall()
            return response
        except:
            raise DbException


db = DatabaseConnection()
