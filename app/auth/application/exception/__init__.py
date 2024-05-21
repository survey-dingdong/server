from core.exceptions import CustomException


class DecodeTokenException(CustomException):
    code = 400
    error_code = "TOKEN__DECODE_ERROR"
    message = "token decode error"


class ExpiredTokenException(CustomException):
    code = 400
    error_code = "TOKEN__EXPIRE_TOKEN"
    message = "expired token"


class InvalidTokenException(CustomException):
    code = 400
    error_code = "TOKEN__INVALID"
    message = "invalid token"
