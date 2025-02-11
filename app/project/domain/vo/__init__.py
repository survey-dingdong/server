from enum import Enum


class ExperimentTypeEnum(Enum):
    ONLINE = "online"
    OFFLINE = "offline"


class ExperimentAttendanceStatusTypeEnum(Enum):
    SCHEDULED = "scheduled"
    NOT_ATTENDED = "not_attended"
    ATTENDED = "attended"
