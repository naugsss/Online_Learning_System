from flask_jwt_extended import jwt_required, get_jwt
from flask_smorest import Blueprint
from flask.views import MethodView

from src.controllers.earning import Earning
from src.controllers.mentor import Mentor
from src.schemas import MentorSchema, EarningSchema

blp = Blueprint("Mentor", "Mentor", description="operation on Mentors")


@blp.route("/mentor")
class MentorTasks(MethodView):
    @jwt_required()
    @blp.arguments(MentorSchema)
    def post(self, mentor_data):
        username = mentor_data["username"]
        mentor = Mentor()
        message = mentor.add_mentor(username)
        return {"message": message}


    @jwt_required()
    # @blp.arguments(EarningSchema(many=True))
    def get(self):
        jwt = get_jwt()
        role = jwt.get("role")
        user_id = jwt.get("user_id")
        earning = Earning()
        # print("role")
        # print(role)
        if role == 1:
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
        elif role == 3:
            print(user_id)
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
