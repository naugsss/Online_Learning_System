from flask import request
from flask_jwt_extended import jwt_required, get_jwt
from flask_smorest import Blueprint, abort
from flask.views import MethodView

from src.controllers.courses import Courses
from src.controllers.earning import Earning
from src.controllers.mentor import Mentor
from src.resources.courses_endpoint import list_course_role_3

blp = Blueprint("Mentor", "Mentor", description="operation on Mentors")


@blp.route("/my_courses")
class MentorCourses(MethodView):
    """function to view mentor courses"""

    @jwt_required()
    def get(self):
        jwt = get_jwt()
        user_id = jwt.get("user_id")
        user_role = jwt.get("role")
        course = Courses()
        if user_role != 3:
            abort(401, message="You are not authorized")
        try:
            content = course.list_course(user_role, user_id)
            if content is None:
                return {"message: ": "You haven't made any course"}
            return list_course_role_3(content)

        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except:
            abort(500, message="An Error Occurred Internally in the Server")


@blp.route("/mentor")
class MentorTasks(MethodView):
    """adding a new mentor"""

    @jwt_required()
    def post(self):
        mentor_data = request.get_json()
        jwt = get_jwt()
        user_role = jwt.get("user_role")
        if user_role != 1:
            return {"message : ": "You are not authorized"}, 401
        username = mentor_data["username"]
        mentor = Mentor()
        message = mentor.add_mentor(username)
        return {"message": message}

    @jwt_required()
    def get(self):
        """view earning of mentor"""

        jwt = get_jwt()
        role = jwt.get("role")
        user_id = jwt.get("user_id")

        if role == 1:
            return view_every_mentor_earning()
        elif role == 3:
            return view_mentor_earning(user_id)
        else:
            return {"message": "You are not authorized"}, 401


def view_mentor_earning(user_id):
    earning = Earning()
    earning = earning.calculate_mentor_earning(user_id)
    if earning is None:
        return {"message": "You haven't made any course till now."}
    response = []
    for value in earning:
        mentor_name = value[0]
        course_name = value[1]
        earning = value[2]

        return_dict = {
            "name": mentor_name,
            "course_name": course_name,
            "earning": earning
        }
        response.append(return_dict)
    return response


def view_every_mentor_earning():
    earning = Earning()
    earning = earning.calculate_all_mentor_earning()
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
            "earning": earning
        }
        response.append(return_dict)
    return response
