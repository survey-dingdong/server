from datetime import date

from pydantic import BaseModel, Field

from app.project.domain.vo.type import ExperimentTypeEnum


class ExperimentTimeSlotRequest(BaseModel):
    id: int = Field(..., description="ID")
    start_time: str = Field(..., description="Experiment start time")
    end_time: str = Field(..., description="Experiment end time")
    max_participants: int = Field(
        ..., description="Maximum number of experiment participants"
    )


class CreateProjectRequest(BaseModel):
    title: str = Field(..., description="Title")


class PatchProjectRequest(BaseModel):
    title: str | None = Field(None, description="Title")
    description: str | None = Field(None, description="Description")
    is_public: bool | None = Field(None, description="Whether the project is public")
    start_date: date | None = Field(None, description="Experiment start date")
    end_date: date | None = Field(None, description="Experiment end date")
    excluded_dates: list[date] | None = Field(
        None, description="Experimental exclusion days"
    )
    timeslots: list[ExperimentTimeSlotRequest] | None = Field(
        None, description="Time information of experiment"
    )
    max_participants: int | None = Field(
        None, description="Maximum number of experiment participants"
    )
    experiment_type: ExperimentTypeEnum | None = Field(None)
    location: str | None = Field(None, description="Experiment location")
