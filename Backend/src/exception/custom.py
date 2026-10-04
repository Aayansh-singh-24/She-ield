from fastapi import status
from src.exception.base import AppException

class UserNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            message = "user not found", 
            status_code = status.HTTP_404_NOT_FOUND, 
            error_code = "USER_NOT_FOUND"
        )


class ContactNotFoundException(AppException):
    def __init__(self):
        super().__init__(
            message = "Trusted Contact Not Found",
            status_code = status.HTTP_404_NOT_FOUND,
            error_code = "CONTACT_NOT_FOUND"
        )


class ContactAlreadyExist(AppException):
    pass

class UnauthorizedException(AppException):
    def __init__(self):
        super().__init__(
            message = "Unauthorized access",
            status_code = status.HTTP_401_UNAUTHORIZED,
            error_code = "UNAUTHORIZED"
        )
