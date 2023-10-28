import os
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
            user_id = self.cursor.lastrowid
            return user_id

        self.cursor.execute(query, val)
        user_id = self.cursor.lastrowid
        return user_id

    def update_db(self, query, val=None):
        if val is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, val)
            return self.cursor.lastrowid

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


try:
    db = DatabaseConnection()
except:
    raise ValueError
