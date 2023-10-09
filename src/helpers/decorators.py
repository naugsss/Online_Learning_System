import functools
from fastapi import status
from fastapi.responses import JSONResponse
from helpers.custom_response import my_custom_error
from helpers.jwt_helpers import extract_token_data


def mentor_only(function):
    @functools.wraps(function)
    async def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        access_token = extract_token_data(request)
        role = access_token.get("role")

        if role != 3:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=my_custom_error(403, "Your do not have required permissions."),
            )
        return await function(*args, **kwargs)

    return wrapper


def admin_only(function):
    @functools.wraps(function)
    async def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        access_token = extract_token_data(request)
        role = access_token.get("role")

        if role != 1:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=my_custom_error(
                    403, "You do not have the required permissions."
                ),
            )
        return await function(*args, **kwargs)

    return wrapper


def handle_errors(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return_value = function(*args, **kwargs)
            return return_value

        except LookupError as error:
            return my_custom_error(409, str(error))
        except ValueError as error:
            return my_custom_error(400, str(error))
        except:
            return my_custom_error(500, "An error occurred internally in the server")
    return wrapper