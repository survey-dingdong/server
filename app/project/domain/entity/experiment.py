from datetime import date

from pydantic import BaseModel, Field

from app.project.domain.vo.type import ExperimentTypeEnum
from core.db import Base

from .project import Project, ProjectRead


class ExperimentProject(Base, Project):
    __tablename__ = "experiment_project"

    @classmethod
    def create(cls, workspace_id: int, title: str) -> "ExperimentProject":
        return cls(
            workspace_id=workspace_id,
            title=title,
        )


class ExperimentTimeSlotRead(BaseModel):
    id: int = Field(..., description="ID")
    start_time: str = Field(..., description="Experiment start time")
    end_time: str = Field(..., description="Experiment end time")
    max_participants: int = Field(
        ..., description="Maximum number of experiment participants"
    )


class ExperimentProjectRead(ProjectRead):
    start_date: date = Field(..., description="Experiment start date")
    end_date: date = Field(..., description="Experiment end date")
    excluded_dates: list[date] = Field(..., description="Experimental exclusion days")
    timeslots: list[ExperimentTimeSlotRead] = Field(
        ..., description="Time information of experiment"
    )
    experiment_type: ExperimentTypeEnum = Field(...)
    location: str = Field(..., description="Experiment location")
    participant_code: str | None = Field(
        None, description="Experiment participant code"
    )
