from core.exceptions import CustomException


class PasswordDoesNotMatchException(CustomException):
    code = 403
    error_code = "USER__PASSWORD_DOES_NOT_MATCH"
    message = "password does not match"


class PasswordNotChangedException(CustomException):
    code = 400
    error_code = "USER__PASSWORD_NOT_CHANGED"
    message = "password not changed"


class DuplicateEmailOrusernameException(CustomException):
    code = 400
    error_code = "USER__DUPLICATE_EMAIL"
    message = "duplicate email"


class UserNotFoundException(CustomException):
    code = 404
    error_code = "USER__NOT_FOUND"
    message = "user not found"


class UnauthorizedAccessException(CustomException):
    code = 401
    error_code = "USER__UNAUTHORIZED_ACCESS"
    message = "Unauthorized access. Please complete email verification first"


class DifferentOAuthProviderException(CustomException):
    code = 409
    error_code = "USER__DIFFERENT_OAUTH_PROVIDER"
    message = "Account already linked with a different OAuth provider."


class OAuthLoginWithPasswordAttemptException(CustomException):
    code = 409
    error_code = "USER__OAUTH_LOGIN_WITH_PASSWORD_ATTEMPT"
    message = (
        "Account created through OAuth. Please log in using the linked OAuth provider."
    )


class UserAlreadyExistsException(CustomException):
    code = 400
    error_code = "USER__ALREADY_EXISTS"
    message = "User already exists with the given credentials"
