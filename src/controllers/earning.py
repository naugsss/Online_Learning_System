from models.database import db
from models.fetch_json_data import JsonData

# db = db()
get_query = JsonData.load_data()


class Earning:

    def calculate_mentor_earning(self, user_id=None):
        if user_id is None:
            result = db.get_from_db(get_query.get("COURSE_DETAILS"))
        else:
            result = db.get_from_db(get_query.get("GET_EARNING_DATA"), (user_id,))
        if result is not None:
            values = []
            for row in result:
                if user_id is None:
                    user_id = row[3]
                name = db.get_from_db(get_query.get("GET_NAME"), (user_id,))
                values.append([name[0][0], row[2], row[0] * row[1]])
            return values
        return None
