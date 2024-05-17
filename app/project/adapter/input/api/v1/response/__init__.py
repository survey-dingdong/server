from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.project.domain.entity.experiment import ExperimentTimeslotRead
from app.project.domain.vo.type import ExperimentAttendanceStatus, ExperimentTypeEnum


class CreateProjectResponse(BaseModel):
    id: int = Field(..., description="ID")


class GetProjectListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID")
    workspace_id: int = Field(..., description="Workspace ID")
    title: str = Field(..., description="Title")
    description: str | None = Field(None, description="Description")
    is_public: bool = Field(..., description="Whether the project is public")
    joined_participants: int = Field(
        ..., description="Number of experiment participants"
    )
    max_participants: int = Field(
        ..., description="Maximum number of experiment participants"
    )
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)


class GetExperimentProjectResponse(BaseModel):
    id: int = Field(..., description="ID")
    title: str = Field(..., description="Title")
    description: str | None = Field(None, description="Description")
    is_public: bool = Field(..., description="Whether the project is public")
    start_date: date | None = Field(..., description="Experiment start date")
    end_date: date | None = Field(..., description="Experiment end date")
    excluded_dates: list[date] = Field(..., description="Experimental exclusion days")
    experiment_timeslots: list[ExperimentTimeslotRead] = Field(
        ..., description="Time information of experiment"
    )
    experiment_type: ExperimentTypeEnum = Field(...)
    location: str | None = Field(..., description="Experiment location")
    participant_code: str = Field(..., description="Experiment participant code")
    created_at: datetime = Field(..., description="Created datetime")
    updated_at: datetime = Field(..., description="Updated datetime")


class GetExperimentParticipantResponse(BaseModel):
    id: int = Field(..., description="Participant ID")
    username: str = Field(..., description="Username")
    reserved_date: str = Field(..., description="Reserved Date")
    attendance_status: ExperimentAttendanceStatus = Field(
        ..., description="Attendance Status"
    )
    created_at: datetime = Field(..., description="Created datetime")
    updated_at: datetime = Field(..., description="Updated datetime")
