def get_error_response(status_code, message):
    """Returns a custom error response"""
    return {
        "error": {
            "code": status_code,
            "message": message,
        },
        "status": "failure",
    }


def get_success_response(status_code, message, token):
    """Returns a custom success response"""
    return {
        "code": status_code,
        "message": message,
        "status": "successful",
        "token": token,
    }
