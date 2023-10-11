import os
import sys
import jsonschema

sys.path.append(os.path.dirname(__file__))
from typing import Optional
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Body, HTTPException, Response, status
from datetime import timedelta, datetime
from jose import jwt, JWTError
from helpers.custom_response import get_error_response, get_success_response
from helpers.validations import validate_request_data, check_if_valid_course_name
from schemas import user_schema, register_schema
from controllers.auth import Login
from environs import Env

env = Env()

env.read_env(path=".env")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORTIHM = os.getenv("ALGORITHM")
router = APIRouter()


@router.post("/register")
def register_user(user_data=Body()):
    login = Login()
    try:
        jsonschema.validate(user_data, register_schema)
    except jsonschema.ValidationError as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=get_error_response(400, "Please enter valid credentials."),
        )

    try:
        is_valid = login.sign_up(
            user_data["name"],
            user_data["email"],
            user_data["username"],
            user_data["password"],
        )
        if is_valid is not None:
            user_data = {"role": is_valid[0], "user_id": is_valid[1]}
            access_token = create_access_token(user_data, timedelta(minutes=60))
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=get_success_response(200, "Account created successfully"),
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=get_error_response(401, "This username already exists"),
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=get_error_response(401, "There was an error authenticating"),
        )


@router.post("/login")
def login_user(response: Response, user_credentials=Body()):
    login = Login()
    validation_response = validate_request_data(user_credentials, user_schema)
    if validation_response:
        return validation_response, 400
    try:
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
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=get_error_response(401, "There was an error authenticating"),
        )


def create_access_token(user_data: dict, expires_delta: Optional[timedelta] = None):
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
