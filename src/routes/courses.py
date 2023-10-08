from fastapi import APIRouter, Body, Request, status, Path
from fastapi.responses import JSONResponse
from helpers.custom_response import my_custom_error
from helpers.jwt_helpers import extract_token_data
from controllers.courses import Courses
from helpers.inputs_and_validations import (
    check_valid_course,
    validate_request_data,
)
from schemas import (
    course_schema,
    approval_schema,
    validate_delete_course_schema,
    feedback_schema,
    faq_schema,
)
from helpers.decorators import admin_only, mentor_only
from helpers.list_courses import list_pending_course
from controllers.feedback import Feedback
from controllers.faq import Faq
from models.database import DatabaseConnection
from models.fetch_json_data import JsonData

DatabaseConnection = DatabaseConnection()
get_query = JsonData.load_data()

router = APIRouter(prefix="", tags=["courses"])


@router.get("/courses")
async def get_courses(request: Request):
    jwt_token_data = extract_token_data(request)
    role = jwt_token_data.get("role")
    user_id = jwt_token_data.get("user_id")
    course = Courses()
    content = course.list_course(4, user_id)

    if role == 1:
        content = course.list_course(1, user_id)
        return list_course_role_1(content)
    else:
        return list_course_role_2_or_role_4(content)


@router.post("/courses")
async def add_course(request: Request, body=Body()):
    user_data = extract_token_data(request)
    user_role = user_data.get("role")
    user_id = user_data.get("user_id")
    course = Courses()
    course_details = body
    if user_role != 3:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=my_custom_error(401, "Invalid credentials"),
        )

    validation_response = validate_request_data(course_details, course_schema)

    if validation_response:
        return validation_response
    try:
        name = course_details.get("name")
        content = course_details.get("content")
        duration = course_details.get("duration")
        price = course_details.get("price")
        response = course.add_course(user_id, name, content, duration, price)
        return {"message": response}

    except LookupError as error:
        return my_custom_error(409, str(error))
    except ValueError as error:
        return my_custom_error(400, str(error))
    except:
        return my_custom_error(500, "An error occurred internally in the server")


@router.put("/courses")
@admin_only
async def approve_courses(request: Request, body=Body()):
    user_data = extract_token_data(request)
    user_id = user_data.get("user_id")
    course = Courses()
    approval_details = body
    validation_response = validate_request_data(approval_details, approval_schema)

    if validation_response:
        return validation_response

    try:
        content = course.list_course(1, user_id)
        name, course_id = check_valid_course(approval_details["course_name"], content)

        if not name or not course_id:
            return my_custom_error(404, "No such course exists.")

        message = course.approve_course(course_id, approval_details["approval_status"])
        return {"message": message}
    except LookupError as error:
        return my_custom_error(409, str(error))
    except ValueError as error:
        return my_custom_error(400, str(error))
    except:
        return my_custom_error(500, "An error occurred internally in the server")


@router.delete("/courses")
@admin_only
async def delete_courses(request: Request, body=Body()):
    course = Courses()
    delete_course_details = body
    validation_response = validate_request_data(
        delete_course_details, validate_delete_course_schema
    )

    if validation_response:
        return validation_response
    try:
        course.delete_course(delete_course_details.get("name"))
        return {"message": "course marked as deactivated successfully."}
    except LookupError as error:
        return my_custom_error(409, str(error))
    except ValueError as error:
        return my_custom_error(400, str(error))
    except:
        return my_custom_error(500, "An error occurred internally in the server")


@router.post("/courses/{course_name}")
async def purchase_course(request: Request, course_name: str = Path()):
    jwt_token_data = extract_token_data(request)
    user_id = jwt_token_data.get("user_id")
    course = Courses()
    try:
        content = course.list_course(4, user_id)
        name, course_id = check_valid_course(course_name, content)
        if not name or not course_id:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content=my_custom_error(401, "No such course exists"),
            )

        message = course.purchase_course(user_id, course_id)
        return {"message": message}
    except LookupError as error:
        return my_custom_error(409, str(error))
    except ValueError as error:
        return my_custom_error(400, str(error))
    except:
        return my_custom_error(500, "An error occurred internally in the server")


@router.get("/pending_courses")
@admin_only
async def pending_courses(request: Request):
    try:
        content = list_pending_course()
        if content is None:
            return {"message": "No pending course"}
        return list_course_role_1(content)
    except LookupError as error:
        return my_custom_error(409, str(error))
    except ValueError as error:
        return my_custom_error(400, str(error))
    except:
        return my_custom_error(500, "An error occurred internally in the server")


@router.get("/courses/{course_name}")
async def view_course_content(request: Request, course_name: str = Path()):
    jwt_token_data = extract_token_data(request)
    user_id = jwt_token_data.get("user_id")
    course = Courses()
    purchased_course = course.view_purchased_course(user_id=user_id)
    if purchased_course is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=my_custom_error(400, "You haven't purchased this course"),
        )
    for course_data in purchased_course:
        if course_data[1].lower() == course_name.lower():
            try:
                content = course.view_course_content(course_data[1])
                return {"content": content}
            except LookupError as error:
                return my_custom_error(409, str(error))
            except ValueError as error:
                return my_custom_error(400, str(error))
            except:
                return my_custom_error(
                    500, "An error occurred internally in the server"
                )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=my_custom_error(
            400, "You haven't purchased this course or no such course exists"
        ),
    )


@router.get("/courses/{course_name}/user_feedback")
async def view_course_feedback(request: Request, course_name: str = Path()):
    jwt_token_data = extract_token_data(request)
    user_id = jwt_token_data.get("user_id")
    course = Courses()
    try:
        content = course.list_course(4, user_id)
        feedback = Feedback()
        name, course_id = check_valid_course(course_name, content)
        if not name or not course_id:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=my_custom_error(404, "No such course exists"),
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

    except LookupError as error:
        return my_custom_error(409, str(error))
    except ValueError as error:
        return my_custom_error(400, str(error))
    except:
        return my_custom_error(500, "An error occurred internally in the server")


@router.post("/courses/{course_name}/user_feedback")
async def add_course_feedback(request: Request, course_name: str = Path(), body=Body()):
    jwt_token_data = extract_token_data(request)
    user_id = jwt_token_data.get("user_id")
    course = Courses()
    feedback = Feedback()
    user_feedback = body
    content = course.list_course(4, user_id)
    validation_response = validate_request_data(user_feedback, feedback_schema)
    if validation_response:
        return validation_response, 400
    purchased_course = course.view_purchased_course(user_id)
    for course in purchased_course:
        if course[1].lower() == course_name.lower():
            try:
                ratings = user_feedback["ratings"]
                comments = user_feedback.get("comments")
                if not comments:
                    comments = "No comments"
                name, course_id = check_valid_course(course_name, content)
                if not name or not course_id:
                    return JSONResponse(
                        status_code=status.HTTP_404_NOT_FOUND,
                        content=my_custom_error(404, "No such course exists"),
                    )

                message = feedback.add_course_feedback(
                    course_id, ratings, comments, user_id
                )
                return {"message": message}
            except LookupError as error:
                return my_custom_error(409, str(error))
            except ValueError as error:
                return my_custom_error(400, str(error))
            except:
                return my_custom_error(
                    500, "An error occurred internally in the server"
                )

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=my_custom_error(403, "You are not allowed to perform this"),
    )


@router.get("/courses/{course_name}/user_faq")
async def view_course_faq(request: Request, course_name: str = Path()):
    jwt_token_data = extract_token_data(request)
    user_id = jwt_token_data.get("user_id")
    course = Courses()
    faq = Faq()
    content = course.list_course(4, user_id)
    name, course_id = check_valid_course(course_name, content)

    if not name or not course_id:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=my_custom_error(404, "No such course exists"),
        )
    faq = faq.view_faq(course_name)
    if faq is None:
        return {"message": "No Faq exists for this course"}
    try:
        response = []
        for val in faq:
            answer = val[14]
            question = val[13]

            return_dict = {"question": question, "answer": answer}
            response.append(return_dict)

        return response
    except LookupError as error:
        return my_custom_error(409, str(error))
    except ValueError as error:
        return my_custom_error(400, str(error))
    except:
        return my_custom_error(500, "An error occurred internally in the server")


@router.post("/courses/{course_name}/user_faq")
@mentor_only
async def add_course_faq(request: Request, course_name: str = Path(), body=Body()):
    course = Courses()
    jwt_token_data = extract_token_data(request)
    user_id = jwt_token_data.get("user_id")
    content = course.list_course(4, user_id)
    faq_data = body
    if faq_data is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=my_custom_error(400, "Please enter correct data"),
        )
    validation_response = validate_request_data(faq_data, faq_schema)
    if validation_response:
        return validation_response
    name, course_id = check_valid_course(course_name, content)

    if not name or not course_id:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=my_custom_error(404, "No such course exists"),
        )

    content = DatabaseConnection.get_from_db(
        get_query.get("GET_FAQ_DETAILS"), (user_id,)
    )
    faq = Faq()
    message = faq.add_faq(
        content, faq_data["question"], faq_data["answer"], course_name
    )

    return {"message": message}


def list_course_role_1(content):
    response = []
    for val in content:
        name = val[1]
        duration = val[3]
        price = val[4]
        rating = val[5]
        status = val[8]
        approval_status = val[6]

        return_dict = {
            "name": name,
            "duration": duration,
            "price": price,
            "rating": rating,
            "status": status,
            "approval status": approval_status,
        }

        response.append(return_dict)
    return response


def list_course_role_3(content):
    response = []
    for val in content:
        name = val[0]
        duration = val[1]
        price = val[2]
        rating = val[3]
        no_of_students = val[4]
        earning = val[5]

        return_dict = {
            "name": name,
            "duration (in hrs.)": duration,
            "price": price,
            "rating": rating,
            "no_of_students": no_of_students,
            "earning (in Rs.)": earning,
        }
        response.append(return_dict)
    return response


def list_course_role_2_or_role_4(content):
    response = []
    for val in content:
        name = val[1]
        duration = val[3]
        price = val[4]
        rating = val[5]

        return_dict = {
            "name": name,
            "duration": duration,
            "price": price,
            "rating": rating,
        }

        response.append(return_dict)
    return response
