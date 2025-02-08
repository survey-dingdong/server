class CustomException(Exception):
    code = 400
    error_code = "BAD_GATEWAY"
    message = "BAD GATEWAY"

    def __init__(self, message: str | None = None) -> None:
        if message is not None:
            self.message = message


class InvalidAccessException(CustomException):
    code = 403
    error_code = "INVALID_ACCESS"
    message = "INVALID ACCESS"
