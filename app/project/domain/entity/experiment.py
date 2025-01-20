from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import (
    DATE,
    JSON,
    Boolean,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Time,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.project.domain.vo import ExperimentAttendanceStatusTypeEnum, ExperimentTypeEnum
from core.db.base import BaseWithInId

if TYPE_CHECKING:
    from app.user.domain.entity.user import User
    from app.workspace.domain.entity.workspace import Workspace


class ExperimentProject(BaseWithInId):
    __tablename__ = "experiment_project"

    workspace_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("workspace.id"),
        index=True,
    )

    title: Mapped[str] = mapped_column(String(64), index=True)

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
        init=False,
    )

    start_date: Mapped[datetime.date | None] = mapped_column(
        DATE, nullable=True, index=True, init=False
    )

    end_date: Mapped[datetime.date | None] = mapped_column(
        DATE, nullable=True, index=True, init=False
    )

    location: Mapped[str | None] = mapped_column(String(255), nullable=True, init=False)

    is_public: Mapped[bool] = mapped_column(Boolean, default=False)

    joined_participants: Mapped[int] = mapped_column(Integer, default=0)

    max_participants: Mapped[int] = mapped_column(Integer, default=0)

    experiment_type: Mapped[ExperimentTypeEnum] = mapped_column(
        Enum(ExperimentTypeEnum),
        default=ExperimentTypeEnum.OFFLINE.value,
    )

    excluded_dates: Mapped[list[str]] = mapped_column(JSON, default_factory=list)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    workspace: Mapped["Workspace"] = relationship(
        "Workspace",
        back_populates="experiment_projects",
        init=False,
        uselist=False,
        lazy="selectin",
    )

    experiment_timeslots: Mapped[list["ExperimentTimeslot"]] = relationship(
        "ExperimentTimeslot",
        back_populates="experiment_project",
        init=False,
        lazy="selectin",
    )

    @classmethod
    def create(cls, workspace_id: int, title: str) -> "ExperimentProject":
        return cls(
            workspace_id=workspace_id,
            title=title,
        )


Index(
    None,
    ExperimentProject.workspace_id,
    ExperimentProject.title,
)


class ExperimentTimeslot(BaseWithInId):
    __tablename__ = "experiment_timeslot"

    experiment_project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("experiment_project.id"),
    )

    start_time: Mapped[datetime.time] = mapped_column(Time, index=True)

    end_time: Mapped[datetime.time] = mapped_column(Time, index=True)

    max_participants: Mapped[int] = mapped_column(Integer)

    experiment_project: Mapped["ExperimentProject"] = relationship(
        "ExperimentProject",
        back_populates="experiment_timeslots",
        init=False,
        lazy="selectin",
    )

    experiment_participant_timeslots: Mapped[
        list["ExperimentParticipantTimeslot"]
    ] = relationship(
        "ExperimentParticipantTimeslot",
        back_populates="experiment_timeslot",
        init=False,
        lazy="selectin",
    )

    @classmethod
    def create(
        cls,
        experiment_project_id: int,
        start_time: datetime.time,
        end_time: datetime.time,
        max_participants: int,
    ) -> "ExperimentTimeslot":
        return cls(
            experiment_project_id=experiment_project_id,
            start_time=start_time,
            end_time=end_time,
            max_participants=max_participants,
        )


UniqueConstraint(
    ExperimentTimeslot.experiment_project_id,
    ExperimentTimeslot.start_time,
    ExperimentTimeslot.end_time,
)


class ExperimentParticipantTimeslot(BaseWithInId):
    __tablename__ = "experiment_participant_timeslot"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id"),
    )

    experiment_timeslot_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("experiment_timeslot.id"),
    )

    experiment_date: Mapped[datetime.date] = mapped_column(DATE, index=True)

    attendance_status: Mapped[ExperimentAttendanceStatusTypeEnum] = mapped_column(
        Enum(ExperimentAttendanceStatusTypeEnum),
        default=ExperimentAttendanceStatusTypeEnum.SCHEDULED,
    )

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="experiment_participant_timeslots",
        init=False,
        uselist=False,
        lazy="selectin",
    )

    experiment_timeslot: Mapped["ExperimentTimeslot"] = relationship(
        "ExperimentTimeslot",
        back_populates="experiment_participant_timeslots",
        init=False,
        uselist=False,
        lazy="selectin",
    )


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

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
    created_at: datetime.datetime = Field(...)
    updated_at: datetime.datetime = Field(...)


class ExperimentTimeslotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    id: int = Field(..., description="ID")
    start_time: datetime.time = Field(..., description="Experiment start datetime.time")
    end_time: datetime.time = Field(..., description="Experiment end datetime.time")
    max_participants: int = Field(
        ..., description="Maximum number of exparticipants per session"
    )


class ExperimentProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    id: int = Field(..., description="ID")
    title: str = Field(..., description="Title")
    description: str | None = Field(None, description="Description")
    is_public: bool = Field(..., description="Whether the project is public")
    start_date: datetime.date | None = Field(
        ..., description="Experiment start datetime.date"
    )
    end_date: datetime.date | None = Field(
        ..., description="Experiment end datetime.date"
    )
    excluded_dates: list[str] = Field(..., description="Experimental exclusion days")
    experiment_timeslots: list[ExperimentTimeslotRead] = Field(
        ..., description="Time information of experiment"
    )
    max_participants: int = Field(
        ..., description="Maximum number of experiment participants"
    )
    experiment_type: ExperimentTypeEnum = Field(...)
    location: str | None = Field(..., description="Experiment location")
    created_at: datetime.datetime = Field(..., description="Created datetime")
    updated_at: datetime.datetime = Field(..., description="Updated datetime")


class ExperimentParticipantTimeslotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    id: int = Field(..., description="Participant ID")
    username: str = Field(..., description="Username")
    profile_color: str = Field(..., description="Profile color")
    experiment_date: datetime.date = Field(..., description="Experiment Date")
    start_time: datetime.time = Field(..., description="Experiment start datetime.time")
    end_time: datetime.time = Field(..., description="Experiment end datetime.time")
    attendance_status: ExperimentAttendanceStatusTypeEnum = Field(
        ..., description="Attendance Status"
    )
    created_at: datetime.datetime = Field(..., description="Created datetime")
    updated_at: datetime.datetime = Field(..., description="Updated datetime")
