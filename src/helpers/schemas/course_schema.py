course_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "content": {
            "type": "string",
            "max_length": 500,
        },
        "duration": {"type": "integer", "minimum": 1},
        "price": {"type": "integer", "minimum": 1},
    },
    "required": ["name", "content", "duration", "price"],
}

purchase_course_schema = {
    "type": "object",
    "properties": {"name": {"type": "string"}},
    "required": ["name"],
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
