from core.exceptions import CustomException


class TooManyWorkspacesException(CustomException):
    code = 400
    error_code = "WORKSPACE__TOO_MANY"
    message = "too many workspaces"


class WrongOrderNoWorkspacesException(CustomException):
    code = 400
    error_code = "WORKSPACE__WRONG_ORDER_NO"
    message = "invalid scope of workspace order_no"


class WorkspaceNotFoundeException(CustomException):
    code = 404
    error_code = "WORKSPACE__NOT_FOUND"
    message = "workspace not found"


class WorkspaceAccessDeniedException(CustomException):
    code = 403
    error_code = "WORKSPACE__ACCESS_DENIED"
    message = "workspace access denied"
