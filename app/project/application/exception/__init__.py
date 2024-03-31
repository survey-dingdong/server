from core.exceptions import CustomException


class ProjectNotFoundeException(CustomException):
    code = 404
    error_code = "PROJECT__NOT_FOUND"
    message = "project not found"
