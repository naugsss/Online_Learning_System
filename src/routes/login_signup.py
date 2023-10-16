import os
from typing import Optional
from datetime import timedelta, datetime
import jsonschema
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Body, Response, status
from jose import jwt
from environs import Env
from src.helpers.handle_error_decorator import handle_errors
from src.helpers.schemas.login_signup_schema import sign_up_schema, login_schema
from src.helpers.custom_response import get_error_response, get_success_response
from src.helpers.validations import validate_request_data
from src.controllers.auth import Login

env = Env()

env.read_env(path=".env")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORTIHM = os.getenv("ALGORITHM")
router = APIRouter()


@handle_errors
@router.post("/register")
def register_user(user_data=Body()):
    """Register a new user"""
    login = Login()
    try:
        jsonschema.validate(user_data, sign_up_schema)
    except jsonschema.ValidationError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=get_error_response(400, "Please enter valid credentials."),
        )

    is_valid = login.sign_up(
        user_data["name"],
        user_data["email"],
        user_data["username"],
        user_data["password"],
    )
    if is_valid is not None:
        user_data = {"role": is_valid[0], "user_id": is_valid[1]}
        create_access_token(user_data, timedelta(minutes=60))
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=get_success_response(200, "Account created successfully"),
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=get_error_response(401, "This username already exists"),
        )


@router.post("/login")
@handle_errors
def login_user(response: Response, user_credentials=Body()):
    """Login a user with the given credentials"""
    login = Login()
    validation_response = validate_request_data(user_credentials, login_schema)
    if validation_response:
        return validation_response
    is_authenticated = login.login_user(
        username=user_credentials["username"], password=user_credentials["password"]
    )
    if is_authenticated is not None:
        user_data = {"role": is_authenticated[0], "user_id": is_authenticated[1]}
        access_token = create_access_token(user_data, timedelta(minutes=60))
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return get_success_response(200, "Login Successfully")

    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=get_error_response(401, "Invalid credentials"),
        )


def create_access_token(user_data: dict, expires_delta: Optional[timedelta] = None):
    """Create a new access token for the given user"""
    print("user_data", user_data)
    encode = {
        "user_id": user_data.get("user_id"),
        "role": user_data.get("role"),
    }

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORTIHM)
