from core.exceptions import CustomException


class TooManyWorkspacesException(CustomException):
    code = 400
    error_code = "WORKSPACE__TOO_MANY"
    message = "too many workspaces"


class WorkspaceNotFoundeException(CustomException):
    code = 404
    error_code = "WORKSPACE__NOT_FOUND"
    message = "workspace not found"
