from flask_smorest import Blueprint, abort
from flask.views import MethodView
from src.controllers.auth import Login
from src.schemas import UserSchema
from flask_jwt_extended import create_access_token

blp = Blueprint("Users", "Users", description="operations on users")


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):

        instance = Login()
        try:
            is_authenticated = instance.login_user(username=user_data["username"], password=user_data["password"])
            # print(is_authenticated)
            if is_authenticated:
                access_token = create_access_token(identity=is_authenticated)
                return {"access_token": access_token}, 200
            return {"message": "You logged into the system successfully."}
        except Exception as error:
            abort(401, message="Invalid credentials.")
    
    
