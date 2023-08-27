from src.models.context_manager import DatabaseConnection


class Authentication:

    def __init__(self, username, password):
        self.username = username
        self.password = password

        try:
            with DatabaseConnection() as db:
                cursor = db.cursor()

                cursor.execute("SELECT * FROM authentication WHERE username = %s", (self.username,))
                result = cursor.fetchone()
                for x in result:
                    print(x)

                print("You logged into the system successfully..")
        except:
            print("No such user exists in the database. ")
