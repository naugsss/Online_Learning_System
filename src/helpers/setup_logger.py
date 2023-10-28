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


class InfoLogger:
    def __init__(self, logger):
        logger = logger
        # file_handler = logging.FileHandler(logger)

    def log(self, message, *args):
        logger.info(message, *args)


class DebugLogger:
    def __init__(self, logger):
        logger = logger

    def log(self, message):
        logger.debug(message)
