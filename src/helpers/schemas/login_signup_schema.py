sign_up_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {
            "type": "string",
            "pattern": r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}",
        },
        "username": {"type": "string"},
        "password": {
            "type": "string",
            "pattern": r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{5,}$",
            "min_length": 5,
        },
    },
    "required": ["name", "email", "username", "password"],
}

login_schema = {
    "type": "object",
    "properties": {"username": {"type": "string"}, "password": {"type": "string"}},
    "required": ["username", "password"],
}
