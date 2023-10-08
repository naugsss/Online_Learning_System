register_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"},
        "username": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["username", "password"],
}

user_schema = {
    "type": "object",
    "properties": {"username": {"type": "string"}, "password": {"type": "string"}},
    "required": ["username", "password"],
}

course_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "content": {"type": "string"},
        "duration": {"type": "integer"},
        "price": {"type": "integer"},
    },
    "required": ["name", "content", "duration", "price"],
}

validate_course_schema = {
    "type": "object",
    "properties": {
        "course_name": {"type": "string"},
        "approval_status": {"type": "string"},
    },
    "required": ["course_name", "approval_status"],
}

purchase_course_schema = {
    "type": "object",
    "properties": {"name": {"type": "string"}},
    "required": ["name"],
}

feedback_schema = {
    "type": "object",
    "properties": {"ratings": {"type": "number"}, "comments": {"type": "string"}},
}

faq_schema = {
    "type": "object",
    "properties": {"question": {"type": "string"}, "answer": {"type": "string"}},
    "required": ["question", "answer"],
}

mentor_schema = {
    "type": "object",
    "properties": {"username": {"type": "string"}},
    "required": ["username"],
}

earning_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "earning": {"type": "integer"},
    },
    "required": ["ratings"],
}

approval_schema = {
    "type": "object",
    "properties": {
        "course_name": {"type": "string"},
        "approval_status": {"type": "string"},
    },
    "required": ["course_name", "approval_status"],
}

validate_delete_course_schema = {
    "type": "object",
    "properties": {"name": {"type": "string"}},
    "required": ["course_name"],
}
