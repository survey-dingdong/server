from core.exceptions import CustomException


class ProjectNotFoundException(CustomException):
    code = 404
    error_code = "PROJECT__NOT_FOUND"
    message = "project not found"


class ProjectAccessDeniedException(CustomException):
    code = 403
    error_code = "PROJECT__ACCESS_DENIED"
    message = "project does not belong to the workspace"


class ParticipantNotFoundException(CustomException):
    code = 404
    error_code = "PARTICIPANT__NOT_FOUND"
    message = "participant not found"


class ParticipantAccessDeniedException(CustomException):
    code = 403
    error_code = "PARTICIPANT__ACCESS_DENIED"
    message = "participant does not belong to the project"
