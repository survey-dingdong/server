from datetime import date, time

from pydantic import BaseModel, Field

from app.project.domain.vo.type import ExperimentTypeEnum


class CreateProjectRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=20, description="Title")


class ExperimentTimeslotRequest(BaseModel):
    id: int | None = Field(None, description="ID")
    start_time: time = Field(..., description="Experiment start time")
    end_time: time = Field(..., description="Experiment end time")
    max_participants: int = Field(
        ..., description="Maximum number of experiment participants"
    )


class PutProjectRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=20, description="Title")
    description: str = Field(..., description="Description")
    is_public: bool = Field(..., description="Whether the project is public")
    start_date: date = Field(..., ddescription="Experiment start date")
    end_date: date = Field(..., description="Experiment end date")
    excluded_dates: list[date] = Field(..., description="Experimental exclusion days")
    experiment_timeslots: list[ExperimentTimeslotRequest] = Field(
        ..., description="Time information of experiment"
    )
    experiment_type: ExperimentTypeEnum = Field(...)
    location: str = Field(..., description="Experiment location")
