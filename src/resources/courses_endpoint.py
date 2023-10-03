from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from flask_smorest import Blueprint
from flask.views import MethodView
from src.controllers.courses import Courses, list_course_in_tabular_form
from src.controllers.faq import Faq
from src.controllers.feedback import Feedback
from src.helpers.inputs_and_validations import validate_request_data, check_valid_course
from src.schemas import feedback_schema, course_schema, validate_course_schema, faq_schema
from src.models.database import DatabaseConnection
from src.models.fetch_json_data import JsonData

DatabaseConnection = DatabaseConnection()

get_query = JsonData.load_data()
blp = Blueprint("Courses", "Courses", description="operations on courses")


@blp.route("/courses")
class Course(MethodView):
    """function to list all the courses present"""

    @jwt_required()
    def get(self):
        jwt = get_jwt()
        role = jwt.get("role")
        user_id = jwt.get("user_id")
        course = Courses()
        content = course.list_course(4, user_id)

        if role == 1:
            content = course.list_course(1, user_id)
            return list_course_role_1(content)
        else:
            return list_course_role_2_or_role_4(content)

    @jwt_required()
    def post(self):
        """function to add a new course"""
        course = Courses()
        jwt = get_jwt()
        user_id = jwt.get("user_id")
        user_data = request.get_json()
        user_role = jwt.get("role")
        if user_role != 3:
            return my_custom_error(403, "You are not allowed to do this")

        validation_response = validate_request_data(user_data, course_schema)
        if validation_response:
            return validation_response

        try:
            response = course.add_course(
                user_id=user_id,
                course_name=user_data["name"],
                content=user_data["content"],
                duration=user_data["duration"],
                price=user_data["price"],
            )
            return {"message": response}

        except LookupError as error:
            return my_custom_error(409, str(error))
        except ValueError as error:
            return my_custom_error(400, str(error))
        except:
            return my_custom_error(500, "An error occurred internally in the server")

    @jwt_required()
    def delete(self):
        """function to mark a course as deactive"""
        course = Courses()
        jwt = get_jwt()
        user_role = jwt.get("role")
        if user_role != 1:
            return my_custom_error(403, "You are not allowed to deactivate a course")

        try:
            user_data = request.get_json()
            course.delete_course(user_data["name"])
            return {"message": "course marked as deactivated successfully."}
        except LookupError as error:
            return my_custom_error(409, str(error))
        except ValueError as error:
            return my_custom_error(400, str(error))
        except:
            return my_custom_error(500, "An error occurred internally in the server")

    @jwt_required()
    def put(self):
        """function to approve a course"""
        course = Courses()
        jwt = get_jwt()
        user_id = jwt.get("user_id")
        user_role = jwt.get("role")
        if user_role != 1:
            return my_custom_error(403, "You are not allowed to do this.")

        course_data = request.get_json()
        validation_response = validate_request_data(course_data, validate_course_schema)
        if validation_response:
            return validation_response, 400

        try:
            content = course.list_course(1, user_id)
            name, course_id = check_valid_course(course_data["course_name"], content)

            if not name or not course_id:
                return my_custom_error(404, "No such course exists.")

            message = course.approve_course(course_id, course_data["approval_status"])
            return {"message": message}
        except LookupError as error:
            return my_custom_error(409, str(error))
        except ValueError as error:
            return my_custom_error(400, str(error))
        except:
            return my_custom_error(500, "An error occurred internally in the server")


@blp.route("/courses/<string:course_name>")
class AccessCourse(MethodView):
    @jwt_required()
    def post(self, course_name):
        """function to purchase a course"""

        course = Courses()
        jwt = get_jwt()
        user_id = jwt.get("user_id")

        try:
            content = course.list_course(4, user_id)
            name, course_id = check_valid_course(course_name, content)
            if not name or not course_id:
                return my_custom_error(401, "No such course exists.")

            message = course.purchase_course(user_id, course_id)
            return {"message": message}
        except LookupError as error:
            return my_custom_error(409, str(error))
        except ValueError as error:
            return my_custom_error(400, str(error))
        except:
            return my_custom_error(500, "An error occurred internally in the server")

    @jwt_required()
    def get(self, course_name):
        """function to access the course content"""
        course = Courses()
        jwt = get_jwt()
        user_id = jwt.get("user_id")
        purchased_course = course.view_purchased_course(user_id=user_id)
        if purchased_course is None:
            return my_custom_error(400, "You haven't purchased any course.")
        for course_data in purchased_course:
            if course_data[1].lower() == course_name.lower():
                try:
                    print("Inside try block")
                    content = course.view_course_content(course_data[1])
                    return {"content": content}
                except LookupError as error:
                    return my_custom_error(409, str(error))
                except ValueError as error:
                    return my_custom_error(400, str(error))
                except:
                    return my_custom_error(
                        500, "An error occurred internally in the server"
                    )

        return my_custom_error(
            403, "No such course exists or you haven't purchased this course."
        )


@blp.route("/courses/<string:course_name>/user_feedback")
class accessFeedback(MethodView):
    @jwt_required()
    def post(self, course_name):
        """function to add feedback to courses"""
        feedback = Feedback()
        course = Courses()
        jwt = get_jwt()
        user_id = jwt.get("user_id")
        content = course.list_course(4, user_id)
        user_feedback = request.get_json()
        validation_response = validate_request_data(user_feedback, feedback_schema)
        if validation_response:
            return validation_response, 400
        purchased_course = course.view_purchased_course(user_id)
        for course in purchased_course:
            if course[1].lower() == course_name.lower():
                try:
                    ratings = user_feedback["ratings"]
                    comments = user_feedback.get("comments")
                    if not comments:
                        comments = "No comments"
                    name, course_id = check_valid_course(course_name, content)
                    if not name or not course_id:
                        return my_custom_error(404, "No such course exists.")

                    message = feedback.add_course_feedback(
                        course_id, ratings, comments, user_id
                    )
                    return {"message": message}
                except LookupError as error:
                    return my_custom_error(409, str(error))
                except ValueError as error:
                    return my_custom_error(400, str(error))
                except:
                    return my_custom_error(
                        500, "An error occurred internally in the server"
                    )

        return my_custom_error(403, "You are not allowed to do this.")

    @jwt_required()
    def get(self, course_name):
        """function to view feedback of courses"""
        jwt = get_jwt()
        user_id = jwt.get("user_id")
        course = Courses()
        try:
            content = course.list_course(4, user_id)
            feedback = Feedback()
            name, course_id = check_valid_course(course_name, content)
            if not name or not course_id:
                return my_custom_error(404, "No such course exists.")

            feedback = feedback.view_course_feedback(course_id)
            if feedback is None:
                return {"message": "No feedback exists for this course"}
            response = []
            for val in feedback:
                rating = val[3]
                comment = val[4]

                return_dict = {"rating": rating, "comment": comment}
                response.append(return_dict)

            return response

        except LookupError as error:
            return my_custom_error(409, str(error))
        except ValueError as error:
            return my_custom_error(400, str(error))
        except:
            return my_custom_error(500, "An error occurred internally in the server")


@blp.route("/pending_courses")
class PendingRequests(MethodView):
    """function to check for any pending course for approval"""

    @jwt_required()
    def get(self):
        jwt = get_jwt()
        role = jwt.get("role")

        if role != 1:
            return my_custom_error(403, "You are not allowed to view this.")

        try:
            content = list_pending_course()
            if content is None:
                return {"message": "No pending course"}
            return list_course_role_1(content)
        except LookupError as error:
            return my_custom_error(409, str(error))
        except ValueError as error:
            return my_custom_error(400, str(error))
        except:
            return my_custom_error(500, "An error occurred internally in the server")


@blp.route("/courses/<string:course_name>/user_faq")
class accessFaq(MethodView):
    @jwt_required()
    def get(self, course_name):
        """function to view FAQ of courses"""
        jwt = get_jwt()
        user_id = jwt.get("user_id")
        course = Courses()
        content = course.list_course(4, user_id)
        faq = Faq()
        name, course_id = check_valid_course(course_name, content)

        if not name or not course_id:
            return my_custom_error(404, "No such course exists.")

        faq = faq.view_faq(course_name)
        if faq is None:
            return {"message": "No Faq exists for this course"}
        try:
            response = []
            for val in faq:
                answer = val[14]
                question = val[13]

                return_dict = {"question": question, "answer": answer}
                response.append(return_dict)

            return response
        except LookupError as error:
            return my_custom_error(409, str(error))
        except ValueError as error:
            return my_custom_error(400, str(error))
        except:
            return my_custom_error(500, "An error occurred internally in the server")

    @jwt_required()
    def post(self, course_name):

        """function to add faq to course"""
        jwt = get_jwt()
        user_id = jwt.get("user_id")
        user_role = jwt.get("role")
        if user_role != 3:
            return my_custom_error(403, "You are not allowed to do this")

        course = Courses()
        content = course.list_course(4, user_id)
        faq_data = request.get_json()
        if faq_data is None:
            return my_custom_error(400, "Please enter correct data")
        validation_response = validate_request_data(faq_data, faq_schema)
        if validation_response:
            return validation_response
        name, course_id = check_valid_course(course_name, content)

        if not name or not course_id:
            return my_custom_error(404, "No such course exists.")

        content = DatabaseConnection.get_from_db(
            get_query.get("GET_FAQ_DETAILS"), (user_id,)
        )
        faq = Faq()
        message = faq.add_faq(
            content, faq_data["question"], faq_data["answer"], course_name
        )

        return {"message": message}


def list_pending_course():
    print("**************************")
    print("Pending Notification : ")
    query = get_query.get("PENDING_STATUS")
    result = DatabaseConnection.get_from_db(query, ("pending",))
    if not result:
        return
    print("Course details : \n")
    headers = ["Name", "Duration (in months)", "Price"]
    included_columns = [1, 3, 4]
    content = list_course_in_tabular_form(
        query, headers, "grid", included_columns, ("pending",)
    )
    return content


def my_custom_error(status_code, message):
    return (
        jsonify(
            {
                "error": {
                    "code": status_code,
                    "message": message,
                },
                "status": "failure",
            }
        ),
        status_code,
    )


def list_course_role_1(content):
    response = []
    for val in content:
        name = val[1]
        duration = val[3]
        price = val[4]
        rating = val[5]
        status = val[8]
        approval_status = val[6]

        return_dict = {
            "name": name,
            "duration": duration,
            "price": price,
            "rating": rating,
            "status": status,
            "approval status": approval_status,
        }

        response.append(return_dict)
    return response


def list_course_role_3(content):
    response = []
    for val in content:
        name = val[0]
        duration = val[1]
        price = val[2]
        rating = val[3]
        no_of_students = val[4]
        earning = val[5]

        return_dict = {
            "name": name,
            "duration (in hrs.)": duration,
            "price": price,
            "rating": rating,
            "no_of_students": no_of_students,
            "earning (in Rs.)": earning,
        }
        response.append(return_dict)
    return response


def list_course_role_2_or_role_4(content):
    response = []
    for val in content:
        name = val[1]
        duration = val[3]
        price = val[4]
        rating = val[5]

        return_dict = {
            "name": name,
            "duration": duration,
            "price": price,
            "rating": rating,
        }

        response.append(return_dict)
    return response
