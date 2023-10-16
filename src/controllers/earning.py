from src.models.database import db
from src.configurations.config import sql_queries


QUERIES = sql_queries


class Earning:
    def calculate_mentor_earning(self, user_id=None):
        """calculates the total earning of a mentor from his course

        Args:
            user_id (int, optional): the user id of the mentor. Defaults to None.

        Returns:
            int/None: returns the total earning of a mentor from his course otherwise None.
        """
        if user_id is None:
            result = db.get_from_db(QUERIES.get("COURSE_DETAILS"))
        else:
            result = db.get_from_db(QUERIES.get("GET_EARNING_DATA"), (user_id,))
        if result is not None:
            values = []
            for row in result:
                if user_id is None:
                    user_id = row[3]
                name = db.get_from_db(QUERIES.get("GET_NAME"), (user_id,))
                values.append([name[0][0], row[2], row[0] * row[1]])
            return values
        return None

    def list_mentor_earning(self, user_id=None):
        """This will return the earning in a proper dictionary format"""

        if user_id is None:
            earning = self.calculate_mentor_earning()
        else:
            earning = self.calculate_mentor_earning(user_id)
        if earning is None:
            return {"message": "There are no mentor as of now."}
        response = []
        for value in earning:
            mentor_name = value[0]
            course_name = value[1]
            earning = value[2]

            return_dict = {
                "name": mentor_name,
                "course_name": course_name,
                "earning": earning,
            }
            response.append(return_dict)
        return response
