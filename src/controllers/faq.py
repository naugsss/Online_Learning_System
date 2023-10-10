from controllers.courses import Courses
from models.database import db
from models.fetch_json_data import JsonData

get_query = JsonData.load_data()

course = Courses()


class Faq:
    def view_faq(self, course_name):
        result = db.get_from_db(get_query.get("GET_FAQ"), (course_name,))
        if result is None or len(result) == 0:
            return None
        else:
            return result

    def add_faq(self, content, question, answer, course_name):
        is_valid_input = False
        for row in content:
            if row[4].lower() == course_name.lower():
                is_valid_input = True

                db.insert_into_db(
                    get_query.get("INSERT_FAQ"), (row[3], question, answer)
                )
                return "FAQ added successfully"
        if not is_valid_input:
            return "No such course exists"
