import logging
import time
import traceback

import flask


class RequestFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        # compute s according to record.levelno
        # for example, by setting self._fmt
        # according to the levelno, then calling
        # the superclass to do the actual formatting
        msg = record.getMessage()
        if record.levelno == logging.DEBUG:
            return f"\033[90m{msg}\033[0m"
        return f'\033[90m{time.strftime("%T")}\033[0m {msg}'


class AppFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        color = 92
        msg = record.getMessage()
        if record.levelno == logging.DEBUG:
            color = 97
        elif record.levelno == logging.INFO:
            color = 0
        elif record.levelno == logging.WARNING:
            color = 93
            msg += f"\n{traceback.format_exc()}"
        elif record.levelno == logging.ERROR:
            color = 91
            msg += f"\n{traceback.format_exc()}"
        elif record.levelno == logging.CRITICAL:
            color = 101
            msg += f"\n{traceback.format_exc()}"

        return f'\033[{color}m * {msg}\033[0m'


def init_app_logger(app: flask.Flask) -> logging.Logger:
    # create a new app logger
    logger = logging.getLogger(app.logger.name)  # pylint: disable=no-member
    logger.root.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    for h in logger.handlers:
        logger.removeHandler(h)
    logger.addHandler(get_app_handler())
    return logger


def init_request_logger(app: flask.Flask) -> logging.Logger:
    # disable default http request logger
    log = logging.getLogger("werkzeug")
    log.disabled = True

    # create a new request logger
    logger = logging.getLogger("request_logger")
    logger.setLevel(logging.DEBUG)
    for h in logger.handlers:
        logger.removeHandler(h)
    logger.addHandler(get_request_handler())
    return logger


def get_app_handler() -> logging.StreamHandler:
    formatter = AppFormatter()
    log_handler = logging.StreamHandler()
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(formatter)
    return log_handler


def get_request_handler() -> logging.StreamHandler:
    formatter = RequestFormatter()
    log_handler = logging.StreamHandler()
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(formatter)
    return log_handler
