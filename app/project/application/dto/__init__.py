from __future__ import annotations

import datetime

from pydantic import BaseModel, Field

from app.project.domain.vo import ExperimentAttendanceStatusTypeEnum, ExperimentTypeEnum
from core.helpers.utils import get_random_color


class CreateProjectResponseDTO(BaseModel):
    id: int | None = Field(None, description="ID")


class GetProjectListResponseDTO(BaseModel):
    id: int
    workspace_id: int
    title: str
    description: str | None
    is_public: bool
    joined_participants: int = Field(
        ..., description="Number of experiment participants"
    )
    max_participants: int = Field(
        ..., description="Maximum number of experiment participants"
    )
    created_at: datetime.datetime
    updated_at: datetime.datetime | None


class ExperimentTimeslotDTO(BaseModel):
    id: int
    start_time: datetime.time
    end_time: datetime.time
    max_participants: int = Field(
        ..., description="Maximum number of participants per session"
    )


class GetProjectResponseDTO(BaseModel):
    id: int
    title: str
    description: str | None
    is_public: bool
    start_date: datetime.date | None
    end_date: datetime.date | None
    excluded_dates: list[datetime.date] = Field(
        ..., description="Experimental exclusion days"
    )
    experiment_timeslots: list[ExperimentTimeslotDTO] = Field(
        ..., description="Time information of experiment"
    )
    max_participants: int = Field(
        ..., description="Maximum number of experiment participants"
    )
    experiment_type: ExperimentTypeEnum
    location: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime | None


class UpdateProjectRequestDTO(BaseModel):
    class ExperimentTimeslot(BaseModel):
        id: int | None = Field(None)
        start_time: datetime.time
        end_time: datetime.time
        max_participants: int

    title: str
    description: str | None
    is_public: bool
    start_date: datetime.date | None
    end_date: datetime.date | None
    excluded_dates: list[datetime.date] = Field(
        ..., description="Experimental exclusion days"
    )
    experiment_timeslots: list[ExperimentTimeslot] = Field(
        ..., description="Time information of experiment"
    )
    max_participants: int = Field(
        ..., description="Maximum number of experiment participants"
    )
    experiment_type: ExperimentTypeEnum
    location: str


class GetExperimentParticipantsResponseDTO(BaseModel):
    id: int
    username: str
    profile_color: str = Field(default_factory=lambda: get_random_color())
    experiment_date: datetime.date
    start_time: datetime.time
    end_time: datetime.time
    attendance_status: ExperimentAttendanceStatusTypeEnum
    created_at: datetime.datetime
    updated_at: datetime.datetime
