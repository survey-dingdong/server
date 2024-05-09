from datetime import date, time

from pydantic import BaseModel, Field

from app.project.domain.vo.type import ExperimentTypeEnum


class CreateProjectResponseDTO(BaseModel):
    id: int | None = Field(None, description="ID")


class ExperimentTimeslotDTO(BaseModel):
    id: int | None = Field(None, description="ID")
    start_time: time = Field(..., description="Experiment start time")
    end_time: time = Field(..., description="Experiment end time")
    max_participants: int = Field(
        ..., description="Maximum number of experiment participants"
    )


class PutProjectRequestDTO(BaseModel):
    title: str = Field(..., description="Title")
    description: str = Field(..., description="Description")
    is_public: bool = Field(..., description="Whether the project is public")
    start_date: date = Field(..., description="Experiment start date")
    end_date: date = Field(..., description="Experiment end date")
    excluded_dates: list[date] = Field(..., description="Experimental exclusion days")
    experiment_timeslots: list[ExperimentTimeslotDTO] = Field(
        ..., description="Time information of experiment"
    )
    experiment_type: ExperimentTypeEnum = Field(...)
    location: str = Field(..., description="Experiment location")
