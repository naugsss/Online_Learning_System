from controllers.mentor import Mentor
from helpers.handle_error_decorator import admin_only, handle_errors, mentor_only
from helpers.jwt_helpers import extract_token_data
from helpers.custom_response import get_error_response
from fastapi import Body, Request, APIRouter
from helpers.validations import validate_request_data
from schemas import mentor_schema
from helpers.mentor_earnings import view_every_mentor_earning
from controllers.courses import Courses
from helpers.list_courses import list_course_role_3
import logging

from helpers.setup_logger import log

router = APIRouter(prefix="", tags=["mentors"])
logger = logging.getLogger(__name__)


@router.post("/mentor")
@admin_only
@log
def add_new_mentor(request: Request, body=Body()):
    mentor_data = body
    validation_response = validate_request_data(mentor_data, mentor_schema)
    if validation_response:
        return validation_response
    username = mentor_data.get("username")
    mentor = Mentor()
    message = mentor.add_mentor(username)
    return {"message": message}


@router.get("/mentor")
@handle_errors
@log
def mentor_earning(request: Request):
    jwt_token_data = extract_token_data(request)
    user_id = jwt_token_data.get("user_id")
    role = jwt_token_data.get("role")
    if role == 1:
        return view_every_mentor_earning()
    elif role == 3:
        return view_every_mentor_earning(user_id)
    else:
        return get_error_response(401, "You are not authorized.")


@router.get("/my_courses")
@mentor_only
async def my_courses(request: Request):
    jwt_token_data = extract_token_data(request)
    user_id = jwt_token_data.get("user_id")
    user_role = jwt_token_data.get("role")
    course = Courses()
    try:
        content = course.list_course(user_role, user_id)
        if content is None:
            return {"message: ": "You haven't made any course"}
        return list_course_role_3(content)

    except LookupError as error:
        return get_error_response(409, str(error))
    except ValueError as error:
        return get_error_response(400, str(error))
    except:
        return get_error_response(500, "An error occurred internally in the server")
