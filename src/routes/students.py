from fastapi import APIRouter, Request
from src.helpers.handle_error_decorator import handle_errors
from src.helpers.jwt_helpers import extract_token_data
from src.controllers.courses import Courses, list_course_by_role


router = APIRouter(prefix="", tags=["students"])


@router.get("/purchased_courses")
@handle_errors
def purchase_courses(request: Request):
    jwt_token_data = extract_token_data(request)
    user_id = jwt_token_data.get("user_id")
    course = Courses()
    content = course.view_purchased_course(user_id)
    if content is None:
        return {"message: ": "You haven't purchased any course"}
    return list_course_by_role(content)
