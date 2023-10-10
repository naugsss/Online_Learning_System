def get_error_response(status_code, message):
    return {
        "error": {
            "code": status_code,
            "message": message,
        },
        "status": "failure",
    }


def get_success_response(status_code, message):
    return {"code": status_code, "message": message, "status": "successful"}
