import functools
from fastapi import status
from fastapi.responses import JSONResponse
from src.helpers.custom_response import get_error_response
from src.helpers.jwt_helpers import extract_token_data
from src.configurations.config import access_control_list
from src.helpers.roles_enum import Roles


def grant_access(fun):
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        token = extract_token_data(request=request)
        role = token.get("role")
        operation = fun.__name__
        if operation in access_control_list.get(str(Roles(role).name)):
            return fun(*args, **kwargs)
        else:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content=get_error_response(
                    status_code=403,
                    message="You do not have the permissions to perform this action.",
                ),
            )

    return wrapper
