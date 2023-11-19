from src.controllers.courses import Courses
from src.helpers.exceptions import BadRequestException, NotFoundException
from src.models.database import db
from src.configurations.config import sql_queries, prompts

PROMPTS = prompts
QUERIES = sql_queries

course = Courses()


class Faq:
    def view_faq(self, course_name):
        """view the faq for a given course

        Args:
            course_name (string): name of the course of which user wants to view faq

        Returns:
            string: faq of the course if exsits.
        """
        try:
            result = db.get_from_db(QUERIES.get("GET_FAQ"), (course_name,))

            if len(result) != 0:
                return result
            else:
                return QUERIES.get("NO_FAQ")
        except:
            raise BadRequestException

    def add_faq(self, content, question, answer, course_name):
        """add a faq for a given course

        Args:
            content (string): data from the database
            question (string): question to add in a course
            answer (string): answer to add in a course for a given question
            course_name (string): name of the course in which faqs will be added

        Returns:
            string: custom message, whether faq added or course does not exist
        """
        try:
            is_valid_input = False
            for row in content:
                if row[4].lower() == course_name.lower():
                    is_valid_input = True

                    db.insert_into_db(
                        QUERIES.get("INSERT_FAQ"), (row[3], question, answer)
                    )
                    return PROMPTS.get("FAQ_ADDED_SUCESS")
            if not is_valid_input:
                return NotFoundException(PROMPTS.get("NO_SUCH_COURSE"))
        except:
            raise BadRequestException
