import logging
from fastapi import Body, Request, APIRouter
from src.controllers.earning import Earning
from src.controllers.mentor import Mentor
from src.helpers.handle_error_decorator import handle_errors
from src.helpers.access_decorator import grant_access
from src.helpers.jwt_helpers import extract_token_data
from src.helpers.custom_response import get_error_response
from src.helpers.schemas.mentor_schema import mentor_schema
from src.helpers.validations import validate_request_data
from src.controllers.courses import Courses, list_course_by_role


router = APIRouter(prefix="", tags=["mentors"])
logger = logging.getLogger(__name__)


@router.post("/mentor")
@grant_access
@handle_errors
def add_new_mentor(request: Request, body=Body()):
    """Add a new mentor"""
    print("add_new_mentor")
    mentor_data = body
    print(mentor_data)
    validation_response = validate_request_data(mentor_data, mentor_schema)
    if validation_response:
        return validation_response
    username = mentor_data.get("username")
    mentor = Mentor()
    message = mentor.add_mentor(username)
    return {"message": message}


@router.get("/mentor")
@handle_errors
def mentor_earning(request: Request):
    """calculate the earning of mentor"""
    jwt_token_data = extract_token_data(request)
    user_id = jwt_token_data.get("user_id")
    role = jwt_token_data.get("role")
    earning = Earning()
    if role == 1:
        return earning.list_mentor_earning()
    elif role == 3:
        return earning.list_mentor_earning(user_id)
    else:
        return get_error_response(401, "You are not authorized.")


@router.get("/my_courses")
@grant_access
@handle_errors
def my_courses(request: Request):
    """mentor can see the list of courses made by him"""
    jwt_token_data = extract_token_data(request)
    user_id = jwt_token_data.get("user_id")
    user_role = jwt_token_data.get("role")
    course = Courses()
    content = course.get_course_list_from_db(user_role, user_id)
    if content is None:
        return {"message: ": "You haven't made any course"}
    return list_course_by_role(content, user_role)
