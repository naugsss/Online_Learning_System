import re
import maskpass

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


class invalidNumberException(Exception):
    """Input can't be less than 0"""
    pass


def get_float_input(message):
    try:
        user_input = float(input(message))
        if user_input < 0:
            raise invalidNumberException
        return user_input
    except invalidNumberException:
        print("input cannot be less than 0.. please try again. ")
        get_int_input(message)
    except:
        print("Wrong input made.. please try again. ")
        get_int_input(message)


def get_int_input(message):
    try:
        user_input = int(input(message))
        if user_input < 0:
            raise invalidNumberException
        return user_input
    except invalidNumberException:
        print("input cannot be less than 0.. please try again. ")
        get_int_input(message)
    except:
        print("Wrong input made.. please try again. ")


def get_string_input(message):
    try:
        # pattern = "^[A-Za-z0-9]+$"
        user_input = input(message)
        # if re.fullmatch(pattern, user_input):
        return user_input
    except:
        print("Wrong input made... please try again. ")
        get_int_input(message)


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
    if re.fullmatch(regex, email):
        return True
    else:
        user_email = get_string_input("Please enter a valid email : ")
        if validate_email(user_email):
            return True
