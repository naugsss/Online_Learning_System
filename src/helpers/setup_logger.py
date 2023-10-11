import functools
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


def log(fun):
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        operation = fun.__name__
        logger.debug(f"{operation} called with {(args, kwargs)}.")
        val = fun(*args, **kwargs)
        logger.debug(f"{operation} returned {val}.")
        return val

    return wrapper
