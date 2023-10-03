from flask_jwt_extended import jwt_required, get_jwt
from flask_smorest import Blueprint
from flask.views import MethodView
from src.controllers.courses import Courses
from src.resources.courses_endpoint import my_custom_error

blp = Blueprint("Student", "Student", description="operation on students")


@blp.route("/purchased_courses")
class MyCourse(MethodView):
    @jwt_required()
    def get(self):
        jwt = get_jwt()
        user_id = jwt.get("user_id")
        instance = Courses()
        try:
            content = instance.view_purchased_course(user_id)
            if content is None:
                return {"message: ": "You haven't purchased any course"}
            return list_my_course(content)
        except LookupError as error:
            return my_custom_error(409, str(error))
        except ValueError as error:
            return my_custom_error(400, str(error))
        except:
            return my_custom_error(500, "An error occurred internally in the server")


def list_my_course(content):
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
