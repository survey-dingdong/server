from datetime import date, datetime

from app.project.domain.entity.experiment import (
    ExperimentParticipantTimeslot,
    ExperimentProject,
    ExperimentTimeslot,
)
from app.project.domain.vo.type import ExperimentAttendanceStatus, ExperimentTypeEnum
from core.helpers.utils import generate_random_uppercase_letters


def make_experiment_project(
    id: int,
    workspace_id: int = 1,
    title: str = "project",
    description: str = "",
    is_public: bool = False,
    is_deleted: bool = False,
    joined_participants: int = 0,
    max_participants: int = 0,
    start_date: str = datetime.now().date().strftime("%Y-%m-%d"),
    end_date: str = datetime.now().date().strftime("%Y-%m-%d"),
    excluded_dates: list[str] = [],
    experiment_timeslots: list[ExperimentTimeslot] = [],
    experiment_type: ExperimentTypeEnum = ExperimentTypeEnum.OFFLINE,
    participant_code: str = generate_random_uppercase_letters(),
    location: str = "location",
    created_at: str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    updated_at: str = datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
):
    return ExperimentProject(
        id=id,
        workspace_id=workspace_id,
        title=title,
        description=description,
        is_public=is_public,
        is_deleted=is_deleted,
        joined_participants=joined_participants,
        max_participants=max_participants,
        start_date=start_date,
        end_date=end_date,
        excluded_dates=excluded_dates,
        experiment_timeslots=experiment_timeslots,
        experiment_type=experiment_type,
        location=location,
        participant_code=participant_code,
        created_at=created_at,
        updated_at=updated_at,
    )


def make_experiment_project_participant(
    id: int,
    user_id: int = 1,
    project_id: int = 1,
    experiment_timeslot_id: int = 1,
    experiment_date: date = datetime.now().date(),
    attendance_status: ExperimentAttendanceStatus = ExperimentAttendanceStatus.ATTENDED,
):
    return ExperimentParticipantTimeslot(
        id=id,
        user_id=user_id,
        experiment_timeslot_id=experiment_timeslot_id,
        experiment_date=experiment_date,
        attendance_status=attendance_status,
        experiment_timeslot=ExperimentTimeslot(experiment_project_id=project_id),
    )
