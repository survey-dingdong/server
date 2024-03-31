from enum import Enum


class ProjectTypeEnum(Enum):
    SURVEY = "survey"
    EXPERIMENT = "experiment"


class ExperimentTypeEnum(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
