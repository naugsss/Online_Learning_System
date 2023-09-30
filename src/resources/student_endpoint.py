from flask_jwt_extended import jwt_required, get_jwt
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from src.controllers.courses import Courses

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
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except:
            abort(500, message="An Error Occurred Internally in the Server")


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
