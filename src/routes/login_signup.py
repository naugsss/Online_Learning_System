import os
import sys
from typing import Optional

from fastapi.responses import JSONResponse

sys.path.append(os.path.dirname(__file__))
from fastapi import APIRouter, Body, HTTPException, Response, status
from datetime import timedelta, datetime
from jose import jwt, JWTError
from helpers.custom_response import my_custom_error, my_custom_success
from helpers.inputs_and_validations import validate_request_data, check_valid_course
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
    validation_response = validate_request_data(user_data, register_schema)
    if validation_response:
        return validation_response, 400
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
                content=my_custom_success(200, "Account created successfully"),
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=my_custom_error(401, "This username already exists"),
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=my_custom_error(401, "There was an error authenticating"),
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
            return my_custom_success(200, "Login Successfully")

        else:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=my_custom_error(401, "Invalid credentials"),
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=my_custom_error(401, "There was an error authenticating"),
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
