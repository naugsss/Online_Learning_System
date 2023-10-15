import functools
import traceback
import logging
from fastapi import status
from fastapi.responses import JSONResponse
from src.helpers.custom_response import get_error_response

logger = logging.getLogger(__name__)


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
                    500, "An Error Occurred Internally in the Server"
                ),
            )

    return wrapper
