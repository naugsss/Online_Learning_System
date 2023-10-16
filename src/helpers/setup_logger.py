import logging

logger = logging.getLogger(__name__)


def initialize_logger():
    logging.basicConfig(
        filename="app.log",
        filemode="a",
        format="%(asctime)s,%(msecs)d %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
    )


# def log(logger):
#     def decorator(fun):
#         @functools.wraps(fun)
#         def wrapper(*args, **kwargs):
#             operation = fun.__name__
#             args_repr = [repr(item) for item in args]
#             kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
#             signature = ", ".join(args_repr + kwargs_repr)
#             logger.debug(f"{operation} called with {signature}.")
#             val = fun(*args, **kwargs)
#             logger.debug(f"{operation} returned {val}.")
#             return val

#         return wrapper

#     return decorator


class InfoLogger:
    def __init__(self):
        self.logger = logger

    def log(self, message, *args):
        self.logger.debug(message, *args)


class DebugLogger:
    def __init__(self):
        self.logger = logger

    def log(self, message):
        self.logger.debug(message)
