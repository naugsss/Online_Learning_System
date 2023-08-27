import mysql.connector


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
