from fastapi.responses import JSONResponse


def my_custom_error(status_code, message):
    return {
        "error": {
            "code": status_code,
            "message": message,
        },
        "status": "failure",
    }


def my_custom_success(status_code, message):
    return {"code": status_code, "message": message, "status": "successful"}
