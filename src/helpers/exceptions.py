"""
Contains all exceptions and error related classes and methods
"""


class NoSuchUserError(LookupError):
    """Raised when a user is not found"""


class LoginError(LookupError):
    """Raised when an error occurs at time of login"""


class AccessDeniedException(Exception):
    """Raised when access is denied"""


class DbException(Exception):
    """Raised when db calls raises an error"""


class NotFoundException(Exception):
    """Raised when something is not found"""


class BadRequestException(Exception):
    """Raised when user gives a bad request"""
