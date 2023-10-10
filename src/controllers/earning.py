from models.database import db
from models.fetch_json_data import JsonData

# db = db()
get_query = JsonData.load_data()


class Earning:
    def calculate_mentor_earning(self, user_id):
        result = db.get_from_db(
            get_query.get("GET_EARNING_DATA"), (user_id,)
        )
        values = []
        if len(result) == 0 or result is None:
            return None
        for row in result:
            name = db.get_from_db(get_query.get("GET_NAME"), (user_id,))
            values.append([name[0][0], row[2], row[0] * row[1]])
        return values

# view mentor earnings data
    def calculate_all_mentor_earning(self):
        result = db.get_from_db(get_query.get("COURSE_DETAILS"))
        if result is not None:
            values = []
            for row in result:
                name = db.get_from_db(
                    get_query.get("GET_NAME"), (row[3],)
                )
                values.append([name[0][0], row[2], row[0] * row[1]])

            return values
        return None
