from fastapi.responses import JSONResponse
from fastapi import status
import jsonschema
from src.helpers.custom_response import get_error_response


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
                elif prop_schema["type"] == "string" and not isinstance(
                    prop_value, str
                ):
                    raise ValueError(f"The '{prop}' field must is not valid")

    except jsonschema.exceptions.ValidationError as e:
        error_message = str(e)
        first_line = error_message.split("\n", maxsplit=1)[0]
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=get_error_response(403, first_line),
        )


def check_if_valid_course_name(course_name, content):
    is_valid_course = False
    course_id = None
    for row in content:
        if row[1].lower() == course_name.lower():
            is_valid_course = True
            course_name = row[1]
            course_id = row[0]

    if not is_valid_course:
        return [None, None]

    return [course_name, course_id]
