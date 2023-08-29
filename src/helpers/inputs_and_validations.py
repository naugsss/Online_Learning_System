import re
import maskpass


class invalidNumberException(Exception):
    """Input can't be less than 0"""
    pass


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
    pattern = '[A-Za-z1-9_]+'
    matcher = re.fullmatch(pattern, username)
    return matcher


def validate_name(name):
    pattern = '[A-Za-z ]+'
    matcher = re.fullmatch(pattern, name)
    return matcher


def get_string_input(message):
    try:
        user_input = input(message)
        if user_input.strip() == '':
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
        print("This is not a valid password.")
        user_password = maskpass.askpass(prompt="Enter your password : ", mask="*")
        if validate_password(user_password):
            return True


def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
        return True
    else:
        user_email = get_string_input("Please enter a valid email : ")
        if validate_email(user_email):
            return True
