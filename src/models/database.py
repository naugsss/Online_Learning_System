from src.models.context_manager import DatabaseConnection


def insert_into_db(query, val=None, message=""):
    try:
        with DatabaseConnection() as db:
            cursor = db.cursor()
            if val is None:
                cursor.execute(query)
            else:
                cursor.execute(query, val)
            response = cursor.fetchall()
        return response
    except:
        print(message)


def update_db(query, val=None, message=""):
    try:
        with DatabaseConnection() as db:
            cursor = db.cursor()
            if val is None:
                cursor.execute(query)
            else:
                cursor.execute(query, val)

    except:
        print(message)


def delete_from_db(query, val=None, message=""):
    try:
        with DatabaseConnection() as db:
            cursor = db.cursor()
            if val is None:
                cursor.execute(query)
            else:
                cursor.execute(query, val)
    except:
        print(message)


def get_from_db(query, val=None, message=""):
    try:
        with DatabaseConnection() as db:
            cursor = db.cursor()
            if val is None:
                cursor.execute(query)
            else:
                cursor.execute(query, val)
            response = cursor.fetchall()
        return response
    except:
        print(message)
