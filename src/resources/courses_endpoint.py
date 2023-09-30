from flask import request
from flask_jwt_extended import jwt_required, get_jwt
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from src.controllers.courses import Courses
from src.controllers.faq import Faq
from src.controllers.feedback import Feedback
from src.helpers.entry_menu import EntryMenu
from src.helpers.inputs_and_validations import validate_request_data
from src.schemas import feedback_schema, course_schema, validate_course_schema

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
            abort(403, message="You are not allowed to access this")
        validation_response = validate_request_data(user_data, course_schema)
        if validation_response:
            return validation_response, 400

        try:
            response = course.add_course(user_id=user_id, course_name=user_data["name"],
                                           content=user_data["content"], duration=user_data["duration"],
                                           price=user_data["price"])
            return {"message": response}

        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except:
            abort(500, message="An Error Occurred Internally in the Server")

    @jwt_required()
    def delete(self):
        """function to mark a course as deactive"""
        course = Courses()
        jwt = get_jwt()
        user_role = jwt.get("role")
        if user_role != 1:
            abort(403, message="You are not allowed to deactivate a course")
        try:
            user_data = request.get_json()
            course.delete_course(user_data["name"])
            return {"message": "course marked as deactivated successfully."}
        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except:
            abort(500, message="An Error Occurred Internally in the Server")

    @jwt_required()
    def put(self):
        """function to approve a course"""
        course = Courses()
        jwt = get_jwt()
        user_id = jwt.get("user_id")
        user_role = jwt.get("role")
        if user_role != 1:
            abort(403, message="You are not allowed to approve a course")
        course_data = request.get_json()
        validation_response = validate_request_data(course_data, validate_course_schema)
        if validation_response:
            return validation_response, 400

        try:
            entrymenu = EntryMenu()
            content = course.list_course(1, user_id)
            name, course_id = entrymenu.check_valid_course(course_data["course_name"], content)

            if not name or not course_id:
                abort(404, message="No such course exists")

            message = course.approve_course(course_id, course_data["approval_status"])
            return {"message": message}
        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except:
            abort(500, message="An Error Occurred Internally in the Server")


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
            "approval status": approval_status
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
            "earning (in Rs.)": earning
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


@blp.route("/courses/<string:course_name>")
class AccessCourse(MethodView):
    @jwt_required()
    def post(self, course_name):
        """function to purchase a course"""

        course = Courses()
        jwt = get_jwt()
        user_id = jwt.get("user_id")
        entrymenu = EntryMenu()
        try:
            content = course.list_course(4, user_id)
            name, course_id = entrymenu.check_valid_course(course_name, content)
            if not name or not course_id:
                abort(404, message="No such course exists")

            message = course.purchase_course(user_id, course_id)
            return {"message": message}
        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except:
            abort(500, message="An Error Occurred Internally in the Server")


    @jwt_required()
    def get(self, course_name):
        """function to access the course content"""
        course = Courses()
        jwt = get_jwt()
        user_id = jwt.get("user_id")
        purchased_course = course.view_purchased_course(user_id)
        print(purchased_course)
        for course in purchased_course:
            if course[1].lower() == course_name.lower():
                try:
                    content = course.view_course_content(course[1])
                    return {"content": content}
                except LookupError as error:
                    abort(409, message=str(error))
                except ValueError as error:
                    abort(400, message=str(error))
                except:
                    abort(500, message="An Error Occurred Internally in the Server")
        abort(403, message="You haven't purchased the course or course name is incorrect")


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
        entrymenu = EntryMenu()
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
                    name, course_id = entrymenu.check_valid_course(course_name, content)
                    if not name or not course_id:
                        abort(404, message="No such course exists")

                    message = feedback.add_course_feedback(course_id, ratings, comments, user_id)
                    return {"message": message}
                except LookupError as error:
                    abort(409, message=str(error))
                except ValueError as error:
                    abort(400, message=str(error))
                except:
                    abort(500, message="An Error Occurred Internally in the Server")
        abort(403, message="You are not allowed to do this")

    @jwt_required()
    def get(self, course_name):
        """function to view feedback of courses"""
        jwt = get_jwt()
        user_id = jwt.get("user_id")
        course = Courses()
        try:
            content = course.list_course(4, user_id)
            entrymenu = EntryMenu()
            feedback = Feedback()
            name, course_id = entrymenu.check_valid_course(course_name, content)
            if not name or not course_id:
                abort(404, message="No such course exists")
            feedback = feedback.view_course_feedback(course_id)
            if feedback is None:
                return {"message": "No feedback exists for this course"}
            response = []
            for val in feedback:
                rating = val[3]
                comment = val[4]

                return_dict = {
                    "rating": rating,
                    "comment": comment
                }
                response.append(return_dict)

            return response

        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except:
            abort(500, message="An Error Occurred Internally in the Server")


@blp.route("/pending_courses")
class PendingRequests(MethodView):
    """function to check for any pending course for approval"""
    @jwt_required()
    def get(self):
        jwt = get_jwt()
        role = jwt.get("role")

        if role != 1:
            abort(403, message="You are not allowed to view this.")
        try:
            menu = EntryMenu()
            content = menu.list_pending_course()
            if content is None:
                return {"message": "No pending course"}
            return list_course_role_1(content)
        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except:
            abort(500, message="An Error Occurred Internally in the Server")


@blp.route("/courses/<string:course_name>/user_faq")
class accessFaq(MethodView):

    @jwt_required()
    def get(self, course_name):
        """function to view FAQ of courses"""
        jwt = get_jwt()
        user_id = jwt.get("user_id")
        course = Courses()
        content = course.list_course(4, user_id)
        entrymenu = EntryMenu()
        faq = Faq()
        name, course_id = entrymenu.check_valid_course(course_name, content)

        if not name or not course_id:
            abort(404, message="No such course exists")

        faq = faq.view_faq(course_name)
        if faq is None:
            return {"message": "No Faq exists for this course"}
        try:
            response = []
            for val in faq:
                answer = val[14]
                question = val[13]

                return_dict = {
                    "question": question,
                    "answer": answer
                }
                response.append(return_dict)

            return response
        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except:
            abort(500, message="An Error Occurred Internally in the Server")
