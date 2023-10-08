from fastapi import APIRouter, Request

from helpers.jwt_helpers import extract_token_data
from controllers.courses import Courses
from helpers.custom_response import my_custom_error
from helpers.list_courses import list_my_course


router = APIRouter(prefix="", tags=["students"])


@router.get("/purchased_courses")
async def purchase_courses(request: Request):
    jwt_token_data = extract_token_data(request)
    user_id = jwt_token_data.get("user_id")
    course = Courses()
    try:
        content = course.view_purchased_course(user_id)
        if content is None:
            return {"message: ": "You haven't purchased any course"}
        return list_my_course(content)
    except LookupError as error:
        return my_custom_error(409, str(error))
    except ValueError as error:
        return my_custom_error(400, str(error))
    except:
        return my_custom_error(500, "An error occurred internally in the server")
