import functools
import traceback
from fastapi import logger, status
from fastapi.responses import JSONResponse
from helpers.custom_response import get_error_response
from helpers.jwt_helpers import extract_token_data


def mentor_only(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        access_token = extract_token_data(request)
        role = access_token.get("role")

        if role != 3:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=get_error_response(
                    403, "You do not have required permissions."
                ),
            )
        return function(*args, **kwargs)

    return wrapper


def admin_only(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        access_token = extract_token_data(request)
        role = access_token.get("role")

        if role != 1:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=get_error_response(
                    403, "You do not have the required permissions."
                ),
            )
        return function(*args, **kwargs)

    return wrapper


# def grant_access(fun):
#     @functools.wraps(fun)
#     def wrapper(*args, **kwargs):
#         request = kwargs.get("request")
#         token = extract_token_data(request=request)
#         role = token.get("role")
#         operation = fun.__name__
#         if operation in access_control_list.get(role):
#             return fun(*args, **kwargs)
#         else:
#             return JSONResponse(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 content=get_error_response(
#                     code=403,
#                     message="You do not have the permissions to perform this action.",
#                 ),
#             )

#     return wrapper


def handle_errors(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return_value = function(*args, **kwargs)
            return return_value

        except LookupError as error:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=get_error_response(409, str(error), "Conflict in the Database"),
            )

        except ValueError as error:
            logger.debug(
                "Error Occurred: {} Method Error: {}".format(
                    function.__name__, traceback.format_exc()
                )
            )

            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=get_error_response(400, str(error), "Bad Request"),
            )

        except Exception as error:
            logger.debug(
                "Error Occurred: {} Method Error: {}".format(
                    function.__name__, traceback.format_exc()
                )
            )

            logger.error(
                "Error Occurred: {} Method Error: {}".format(
                    function.__name__, str(error)
                )
            )

            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=get_error_response(
                    500, str(error), "An Error Occurred Internally in the Server"
                ),
            )

    return wrapper
