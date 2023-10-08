import re
from fastapi.responses import JSONResponse
import jsonschema
from fastapi import status
from helpers.custom_response import my_custom_error


class invalidNumberException(Exception):
    """Input can't be less than 0"""

    pass


def validate_request_data(request_data, schema):
    try:
        jsonschema.validate(instance=request_data, schema=schema)
        for prop, prop_schema in schema["properties"].items():
            if prop in request_data:
                prop_value = request_data[prop]
                if prop_schema["type"] == "integer" and not isinstance(prop_value, int):
                    raise ValueError(f"The '{prop}' field must be an integer.")
                elif prop_schema["type"] == "string" and not isinstance(
                    prop_value, str
                ):
                    raise ValueError(f"The '{prop}' field must be a string.")
                elif prop_schema["type"] == "number" and not isinstance(
                    prop_value, float
                ):
                    raise ValueError(f"The '{prop}' field must be a Float value.")

    except jsonschema.exceptions.ValidationError as e:
        error_message = str(e)
        first_line = error_message.split("\n")[0]
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=my_custom_error(403, first_line),
        )


def get_float_input(message):
    try:
        user_input = float(input(message))
        if user_input <= 0:
            raise invalidNumberException
        return user_input
    except invalidNumberException:
        print("input cannot be less than 0.. please try again. ")
        get_float_input(message)
    except:
        print("Wrong input made.. please try again. ")
        get_float_input(message)


def validate_username(username):
    pattern = "[A-Za-z1-9_]+"
    matcher = re.fullmatch(pattern, username)
    return matcher


def validate_name(name):
    pattern = "[A-Za-z ]+"
    matcher = re.fullmatch(pattern, name)
    return matcher


def get_string_input(message):
    try:
        user_input = input(message)
        if user_input.strip() == "":
            print("Input cannot be empty. Please try again.")
            user_input = get_string_input(message)
        return user_input
    except:
        print("Wrong input made... please try again. ")
        return get_string_input(message)


def validate_password(password):
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{5,}$"
    if re.match(pattern, password):
        return True
    else:
        return "This is not a valid password."


def validate_email(email):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    if re.fullmatch(regex, email):
        return True
    else:
        return "This is not a valid email."


def input_user_name(self):
    self.username = input("Enter your username : ")
    is_valid_username = validate_username(self.username)
    if is_valid_username is None:
        print("Enter a valid username...")
        self.input_user_name()


def input_name(self):
    self.name = input("Enter your name : ")
    is_valid_name = validate_name(self.name)
    if is_valid_name is None:
        print("Enter a valid name...")
        self.input_name()


def check_valid_course(course_name, content):
    is_valid_course = False
    course_id = None
    for row in content:
        if row[1].lower() == course_name.lower():
            is_valid_course = True
            course_name = row[1]
            course_id = row[0]

    if not is_valid_course:
        return [None, None]
    else:
        return [course_name, course_id]
