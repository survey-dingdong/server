from enum import Enum, StrEnum


class ProjectTypeEnum(StrEnum):
    SURVEY = "survey"
    EXPERIMENT = "experiment"


class ExperimentTypeEnum(Enum):
    ONLINE = "online"
    OFFLINE = "offline"


class ExperimentAttendanceStatus(Enum):
    SCHEDULED = "scheduled"
    NOT_ATTENDED = "not_attended"
    ATTENDED = "attended"
