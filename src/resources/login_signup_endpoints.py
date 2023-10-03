from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from src.controllers.auth import Login
from flask_jwt_extended import create_access_token
from src.helpers.inputs_and_validations import validate_request_data
from src.resources.courses_endpoint import my_custom_error
from src.schemas import user_schema, register_schema

blp = Blueprint("Users", "Users", description="operations on users")


@blp.route("/login")
class UserLogin(MethodView):
    def post(self):
        login = Login()
        user_data = request.get_json()
        validation_response = validate_request_data(user_data, user_schema)
        if validation_response:
            return validation_response, 400
        try:
            is_authenticated = login.login_user(
                username=user_data["username"], password=user_data["password"]
            )
            print(is_authenticated)
            if is_authenticated is not None:
                access_token = create_access_token(identity=is_authenticated)
                return {"access_token": access_token}, 200
            else:
                return {"message": "You entered wrong credentials."}, 401
        except:
            return my_custom_error(409, "Invalid credentials")


@blp.route("/register")
class UserRegister(MethodView):
    def post(self):
        login = Login()
        user_data = request.get_json()
        validation_response = validate_request_data(user_data, register_schema)
        if validation_response:
            return validation_response, 400
        is_valid = login.sign_up(
            user_data["name"],
            user_data["email"],
            user_data["username"],
            user_data["password"],
        )
        if is_valid:
            access_token = create_access_token(identity=is_valid)
            return {"access_token": access_token}, 200
        return my_custom_error(401, "This username already exists.")
