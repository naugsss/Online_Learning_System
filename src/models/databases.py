from src.models.context_manager import DatabaseConnection
from datetime import date
import hashlib


def add_user_details(name, email, username, password):
    try:
        with DatabaseConnection() as db:
            cursor = db.cursor()
            sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
            val = (name, email)
            cursor.execute(sql, val)
            user_id = cursor.lastrowid
            print("user id : ", user_id)

            sql = "INSERT INTO user_roles (uid, role_id) VALUES (%s, %s)"
            val = (user_id, 4)
            cursor.execute(sql, val)
            print("Inserted into user roles")

            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            sql = "INSERT INTO authentication (username, password, uid, create_at) VALUES (%s, %s, %s, %s)"
            val = (username, hashed_password, user_id, date.today())
            cursor.execute(sql, val)

            print("**** Account created successfully ****")
            return user_id
    except:
        print("An error occurred while inserting into database. Please try again..")
        return False


def validate_user(username, password):
    # adding data to authentication table
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    try:
        with DatabaseConnection() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM authentication WHERE username = %s", (username,))
            response = cursor.fetchone()
            if response[2] == hashed_password:
                print("You logged into the system successfully.")
                return get_role(response[3])
            else:
                print("You entered wrong password. ")
    except:
        print("Error occurred while inserting data. ")


def get_role(user_id):
    try:
        with DatabaseConnection() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM user_roles WHERE uid = %s", (user_id,))
            result = cursor.fetchone()
            role_id = result[2]
            return [role_id, user_id]
    except:
        print("Couldn't fetch a role.")

