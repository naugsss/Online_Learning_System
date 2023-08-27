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
        get_int_input(message)


def get_string_input(message):
    try:
        user_input = input(message)
        return user_input
    except:
        print("Wrong input made... please try again. ")
