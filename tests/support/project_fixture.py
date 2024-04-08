from datetime import date, datetime

from app.project.domain.entity.experiment import (
    ExperimentParticipantTimeSlot,
    ExperimentProject,
)
from app.project.domain.vo.type import ExperimentAttendanceStatus, ExperimentTypeEnum
from core.helpers.utils import generate_random_uppercase_letters


def make_experiment_project(
    id: int,
    workspace_id: int = 1,
    title: str = "project",
    description: str | None = None,
    is_public: bool | None = False,
    max_participants: int | None = 0,
    start_date: date | None = datetime.now().date(),
    end_date: date | None = datetime.now().date(),
    excluded_dates: list[str] | None = [],
    experiment_type: ExperimentTypeEnum | None = ExperimentTypeEnum.OFFLINE,
    participant_code: str | None = generate_random_uppercase_letters(),
    location: str | None = "location",
    created_at: datetime | None = datetime.now(),
    updated_at: datetime | None = datetime.now(),
):
    return ExperimentProject(
        id=id,
        workspace_id=workspace_id,
        title=title,
        description=description,
        is_public=is_public,
        max_participants=max_participants,
        start_date=start_date,
        end_date=end_date,
        excluded_dates=excluded_dates,
        experiment_type=experiment_type,
        location=location,
        participant_code=participant_code,
        created_at=created_at,
        updated_at=updated_at,
    )


def make_experiment_project_participant(
    id: int,
    user_id: int | None = 1,
    experiment_time_slot_id: int | None = 1,
    experiment_date: date | None = datetime.now().date(),
    attendance_status: (
        ExperimentAttendanceStatus | None
    ) = ExperimentAttendanceStatus.ATTENDED,
):
    return ExperimentParticipantTimeSlot(
        id=id,
        user_id=user_id,
        experiment_time_slot_id=experiment_time_slot_id,
        experiment_date=experiment_date,
        attendance_status=attendance_status,
    )
