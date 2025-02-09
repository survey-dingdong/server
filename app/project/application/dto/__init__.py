from __future__ import annotations

import datetime
from datetime import date, time

from pydantic import BaseModel, Field

from app.project.domain.vo import ExperimentTypeEnum


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
    updated_at: datetime.datetime


class ExperimentTimeslotDTO(BaseModel):
    id: int | None
    start_time: time
    end_time: time
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
    excluded_dates: list[str] = Field(..., description="Experimental exclusion days")
    experiment_timeslots: list[ExperimentTimeslotDTO] = Field(
        ..., description="Time information of experiment"
    )
    max_participants: int = Field(
        ..., description="Maximum number of experiment participants"
    )
    experiment_type: ExperimentTypeEnum
    location: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UpdateProjectRequestDTO(BaseModel):
    title: str = Field(..., description="Title")
    description: str | None = Field(None, description="Description")
    is_public: bool = Field(..., description="Whether the project is public")
    start_date: date | None = Field(None, description="Experiment start date")
    end_date: date | None = Field(None, description="Experiment end date")
    excluded_dates: list[date] = Field(..., description="Experimental exclusion days")
    experiment_timeslots: list[ExperimentTimeslotDTO] = Field(
        ..., description="Time information of experiment"
    )
    max_participants: int = Field(
        ..., description="Maximum number of experiment participants"
    )
    experiment_type: ExperimentTypeEnum = Field(...)
    location: str = Field(..., description="Experiment location")
