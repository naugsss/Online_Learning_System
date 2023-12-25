import logging
from fastapi import APIRouter, Body, Request, status, Path
from fastapi.responses import JSONResponse

from src.helpers.schemas.feedback_schema import feedback_schema
from src.helpers.schemas.course_schema import (
    course_schema,
    approval_schema,
)
from src.helpers.schemas.faq_schema import faq_schema
from src.helpers.custom_response import get_custom_success_response, get_error_response
from src.helpers.jwt_helpers import extract_token_data
from src.controllers.courses import Courses, list_course_by_role
from src.helpers.setup_logger import InfoLogger
from src.helpers.validations import (
    check_if_valid_course_name,
    validate_request_data,
)
from src.helpers.handle_error_decorator import handle_errors
from src.helpers.access_decorator import grant_access
from src.controllers.feedback import Feedback
from src.controllers.faq import Faq
from src.models.database import db
from src.configurations.config import sql_queries
from src.helpers.roles_enum import Roles
from src.configurations.config import sql_queries, prompts

PROMPTS = prompts

logger = logging.getLogger(__name__)
QUERIES = sql_queries
router = APIRouter(prefix="", tags=["courses"])
course = Courses()
feedback = Feedback()
info_logger = InfoLogger(logger)


@router.get("/courses")
@handle_errors
def get_courses(request: Request, page=None, size=None):
    jwt_token_data = extract_token_data(request)

    if jwt_token_data == None:
        content, total_count = course.get_course_list_from_db(role=4, page=1, size=4)
        return list_course_by_role(content)

    role = jwt_token_data.get("role")
    user_id = jwt_token_data.get("user_id")
    if page is not None:
        try:
            page = int(page)
        except ValueError:
            raise ValueError(400, "Invalid page parameter")
    if size is not None:
        try:
            size = int(size)
        except ValueError:
            raise ValueError(400, "Invalid size parameter")

    content, total_count = course.get_course_list_from_db(4, user_id, page, size)

    if role == Roles.ADMIN.value:
        info_logger.log("function called admin")
        content, total_count = course.get_course_list_from_db(
            Roles.ADMIN.value, user_id, page, size
        )

        return list_course_by_role(content, Roles.ADMIN.value)
    else:
        return list_course_by_role(content)


@router.post("/courses")
@grant_access
@handle_errors
def add_course(request: Request, body=Body()):
    user_data = extract_token_data(request)
    user_id = user_data.get("user_id")
    course_details = body

    validation_response = validate_request_data(course_details, course_schema)

    if validation_response:
        logger.debug(f"not valid course schema")
        return validation_response
    name = course_details.get("name")
    content = course_details.get("content")
    duration = course_details.get("duration")
    price = course_details.get("price")
    message, status_code = course.add_course(user_id, name, content, duration, price)

    if status_code == 409:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=get_error_response(409, PROMPTS.get("COURSE_ALREADY_EXISTS")),
        )

    elif status_code == 201:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=get_custom_success_response(
                201, PROMPTS.get("COURSE_APPROVAL_REQUEST")
            ),
        )


@router.put("/courses")
@grant_access
@handle_errors
def approve_courses(request: Request, body=Body()):
    user_data = extract_token_data(request)
    user_id = user_data.get("user_id")
    approval_details = body
    validation_response = validate_request_data(approval_details, approval_schema)
    if validation_response:
        logger.debug(f"not valid approval schema --> {validation_response}")
        return validation_response

    content = course.get_course_list_from_db(1, user_id)
    name, course_id = check_if_valid_course_name(
        approval_details.get("course_name"), content
    )
    if not name or not course_id:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=get_error_response(404, "No such course exists"),
        )

    message, status_code = course.approve_course(
        course_id, approval_details["approval_status"]
    )
    if status_code == 202:
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content=get_custom_success_response(202, PROMPTS.get("COURSE_APPROVED")),
        )
    elif status_code == 200:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=get_custom_success_response(200, PROMPTS.get("COURSE_REJECTED")),
        )


@router.put("/courses/{course_name}")
@grant_access
@handle_errors
def delete_courses(request: Request, course_name: str = Path()):
    user_data = extract_token_data(request)
    user_id = user_data.get("user_id")

    content = course.get_course_list_from_db(1, user_id)
    name, course_id = check_if_valid_course_name(course_name, content)

    if not name or not course_id:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=get_error_response(404, "No such course exists"),
        )
    message, status_code = course.delete_course(course_name)
    if status_code == status.HTTP_200_OK:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=get_custom_success_response(
                200,
                PROMPTS.get("COURSE_DEACTIVATED"),
            ),
        )


@router.post("/courses/{course_name}")
@handle_errors
def purchase_course(request: Request, course_name: str = Path()):
    jwt_token_data = extract_token_data(request)
    user_id = jwt_token_data.get("user_id")

    content = course.get_course_list_from_db(4, user_id)
    name, course_id = check_if_valid_course_name(course_name, content)
    if not name or not course_id:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=get_error_response(404, "No such course exists"),
        )

    message, status_code = course.purchase_course(user_id, course_id)
    if status_code == 409:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=get_error_response(409, PROMPTS.get("COURSE_ALREADY_PURCHASED")),
        )
    elif status_code == 200:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=get_custom_success_response(
                200, PROMPTS.get("COURSE_PURCHASED_SUCESS")
            ),
        )


@router.get("/pending_courses")
@grant_access
@handle_errors
def pending_courses(request: Request):
    content = list_pending_course()
    if content is None:
        return {"message": "No pending course"}
    return list_course_by_role(content)


@router.get("/courses/{course_name}")
@handle_errors
def view_course_content(request: Request, course_name: str = Path()):
    jwt_token_data = extract_token_data(request)
    user_id = jwt_token_data.get("user_id")
    purchased_course = course.view_purchased_course(user_id=user_id)
    if purchased_course is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=get_error_response(400, "You haven't purchased this course"),
        )
    for course_data in purchased_course:
        if course_data[1].lower() == course_name.lower():
            content = course.view_course_content(course_data[1])
            return {"content": content}

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=get_error_response(
            400, "You haven't purchased this course or no such course exists"
        ),
    )


@router.get("/courses/{course_name}/user_feedback")
@handle_errors
def view_course_feedback(request: Request, course_name: str = Path()):
    jwt_token_data = extract_token_data(request)

    user_id = jwt_token_data.get("user_id")

    content = course.get_course_list_from_db(4, user_id)
    feedback = Feedback()
    name, course_id = check_if_valid_course_name(course_name, content)
    if not name or not course_id:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=get_error_response(404, "No such course exists"),
        )

    feedback = feedback.view_course_feedback(course_id)
    if feedback is None:
        return {"message": "No feedback exists for this course"}
    response = []
    for val in feedback:
        rating = val[3]
        comment = val[4]

        return_dict = {"rating": rating, "comment": comment}
        response.append(return_dict)

    return response


@router.post("/courses/{course_name}/user_feedback")
@handle_errors
def add_course_feedback(request: Request, course_name: str = Path(), body=Body()):
    jwt_token_data = extract_token_data(request)
    user_id = jwt_token_data.get("user_id")
    user_feedback = body
    course = Courses()
    content = course.get_course_list_from_db(1, user_id)
    validation_response = validate_request_data(user_feedback, feedback_schema)
    if validation_response:
        logger.debug(f"not valid feedback schema --> {validation_response}")
        return validation_response, 400
    purchased_course = course.view_purchased_course(user_id)
    for course in purchased_course:
        if course[1].lower() == course_name.lower():
            ratings = int(user_feedback["ratings"])

            comments = user_feedback.get("comments")
            if not comments:
                comments = "No comments"
            name, course_id = check_if_valid_course_name(course_name, content)
            if not name or not course_id:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content=get_error_response(404, "No such course exists"),
                )

            message, status_code = feedback.add_course_feedback(
                course_id, ratings, comments, user_id
            )

            if status_code == 200:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content=get_custom_success_response(
                        200, PROMPTS.get("FEEDBACK_ADDED_SUCESS")
                    ),
                )
            elif status_code == 409:
                return JSONResponse(
                    status_code=status.HTTP_409_CONFLICT,
                    content=get_custom_success_response(
                        409, PROMPTS.get("ALREADY_ADDED_FEEDBACK")
                    ),
                )

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=get_error_response(403, "You are not allowed to perform this"),
    )


@router.get("/courses/{course_name}/user_faq")
@handle_errors
def view_course_faq(request: Request, course_name: str = Path()):
    jwt_token_data = extract_token_data(request)
    user_id = jwt_token_data.get("user_id")
    faq = Faq()
    content = course.get_course_list_from_db(1, user_id)
    name, course_id = check_if_valid_course_name(course_name, content)

    if not name or not course_id:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=get_error_response(404, "No such course exists"),
        )
    faq = faq.view_faq(course_name)
    if faq is None:
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content=get_custom_success_response(404, "No faq exists for this course"),
        )
    response = []
    for val in faq:
        answer = val[14]
        question = val[13]

        return_dict = {"question": question, "answer": answer}
        response.append(return_dict)

    return response


@router.post("/courses/{course_name}/user_faq")
@grant_access
@handle_errors
def add_course_faq(request: Request, course_name: str = Path(), body=Body()):
    jwt_token_data = extract_token_data(request)
    user_id = jwt_token_data.get("user_id")
    content = course.get_course_list_from_db(3, user_id)
    faq_data = body
    print(faq_data)
    if faq_data is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=get_error_response(400, "Please enter correct data"),
        )
    validation_response = validate_request_data(faq_data, faq_schema)
    if validation_response:
        logger.debug(f"not valid FAQ schema --> {validation_response}")
        return validation_response
    name, course_id = check_if_valid_course_name(course_name, content)

    if not name or not course_id:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=get_error_response(404, "No such course exists"),
        )

    content = db.get_from_db(QUERIES.get("GET_FAQ_DETAILS"), (user_id,))
    faq = Faq()
    message, status_code = faq.add_faq(
        content, faq_data["question"], faq_data["answer"], course_name
    )
    if status_code == 200:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=get_custom_success_response(200, PROMPTS.get("FAQ_ADDED_SUCESS")),
        )


def list_pending_course():
    query = QUERIES.get("PENDING_STATUS")
    result = db.get_from_db(query, ("pending",))
    return result
