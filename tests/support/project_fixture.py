import datetime

from app.project.application.dto import UpdateProjectRequestDTO
from app.project.domain.entity.project import (
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
    excluded_dates: list[datetime.date] = [],
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


def make_experiment_timeslot(
    id: int,
    start_time: datetime.time = datetime.datetime.now().time(),
    end_time: datetime.time = datetime.datetime.now().time(),
    max_participants: int = 0,
) -> UpdateProjectRequestDTO.ExperimentTimeslot:
    experiment_timeslot = UpdateProjectRequestDTO.ExperimentTimeslot(
        id=id,
        start_time=start_time,
        end_time=end_time,
        max_participants=max_participants,
    )
    return experiment_timeslot


def make_experiment_project_participant(
    id: int,
    user_id: int = 1,
    experiment_timeslot_id: int = 1,
    experiment_date: datetime.date = datetime.datetime.now().date(),
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
