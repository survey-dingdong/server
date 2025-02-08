from datetime import date, datetime

from app.project.domain.entity.experiment import (
    ExperimentParticipantTimeslot,
    ExperimentProject,
)
from app.project.domain.vo import ExperimentAttendanceStatusTypeEnum, ExperimentTypeEnum


def make_experiment_project(
    id: int,
    workspace_id: int = 1,
    title: str = "project",
    is_public: bool = False,
    is_deleted: bool = False,
    joined_participants: int = 0,
    max_participants: int = 0,
    excluded_dates: list[str] = [],
    experiment_type: ExperimentTypeEnum = ExperimentTypeEnum.OFFLINE,
) -> ExperimentProject:
    experiment_project = ExperimentProject(
        workspace_id=workspace_id,
        title=title,
        is_public=is_public,
        is_deleted=is_deleted,
        joined_participants=joined_participants,
        max_participants=max_participants,
        excluded_dates=excluded_dates,
        experiment_type=experiment_type,
    )
    experiment_project.id = id
    return experiment_project


def make_experiment_project_participant(
    id: int,
    user_id: int = 1,
    experiment_timeslot_id: int = 1,
    experiment_date: date = datetime.now().date(),
    attendance_status: ExperimentAttendanceStatusTypeEnum = ExperimentAttendanceStatusTypeEnum.ATTENDED,
) -> ExperimentParticipantTimeslot:
    experiment_participant_timeslot = ExperimentParticipantTimeslot(
        user_id=user_id,
        experiment_timeslot_id=experiment_timeslot_id,
        experiment_date=experiment_date,
        attendance_status=attendance_status,
    )
    experiment_participant_timeslot.id = id
    return experiment_participant_timeslot
