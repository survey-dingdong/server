from __future__ import annotations

from datetime import date, datetime, time
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field
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
from app.workspace.domain.entity.workspace import Workspace
from core.db import Base
from core.db.mixins import TimestampMixin

from .project import Project

if TYPE_CHECKING:
    from app.user.domain.entity.user import User


class ExperimentProject(Base, Project):
    __tablename__ = "experiment_project"

    start_date: Mapped[date] = mapped_column(DATE, nullable=True, index=True)
    end_date: Mapped[date] = mapped_column(DATE, nullable=True, index=True)
    excluded_dates: Mapped[list[str]] = mapped_column(JSON, nullable=True, default=[])
    experiment_type: Mapped[ExperimentTypeEnum] = mapped_column(
        Enum(ExperimentTypeEnum),
        nullable=False,
        default=ExperimentTypeEnum.OFFLINE.value,
    )
    location: Mapped[str] = mapped_column(String(255), nullable=True)

    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    workspace: Mapped["Workspace"] = relationship(
        "Workspace",
        back_populates="experiment_projects",
        uselist=False,
        lazy="selectin",
    )
    experiment_timeslots: Mapped[list["ExperimentTimeslot"]] = relationship(
        "ExperimentTimeslot",
        back_populates="experiment_project",
        lazy="selectin",
    )

    @classmethod
    def create(cls, workspace_id: int, title: str) -> "ExperimentProject":
        return cls(
            workspace_id=workspace_id,
            title=title,
        )

    __table_args__ = (Index("idx_workspace_id_title", "workspace_id", "title"),)


class ExperimentTimeslot(Base, TimestampMixin):
    __tablename__ = "experiment_timeslot"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    experiment_project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("experiment_project.id"),
    )
    start_time: Mapped[time] = mapped_column(Time, nullable=False, index=True)
    end_time: Mapped[time] = mapped_column(Time, nullable=False, index=True)
    max_participants: Mapped[int] = mapped_column(Integer, nullable=False)

    experiment_project: Mapped["ExperimentProject"] = relationship(
        "ExperimentProject", back_populates="experiment_timeslots", lazy="selectin"
    )

    experiment_participant_timeslots: Mapped[
        list["ExperimentParticipantTimeslot"]
    ] = relationship(
        "ExperimentParticipantTimeslot",
        back_populates="experiment_timeslot",
        lazy="selectin",
    )

    __table_args__ = (
        UniqueConstraint("experiment_project_id", "start_time", "end_time"),
    )

    @classmethod
    def create(
        cls,
        experiment_project_id: int,
        start_time: time,
        end_time: time,
        max_participants: int,
    ) -> "ExperimentTimeslot":
        return cls(
            experiment_project_id=experiment_project_id,
            start_time=start_time,
            end_time=end_time,
            max_participants=max_participants,
        )


class ExperimentParticipantTimeslot(Base, TimestampMixin):
    __tablename__ = "experiment_participant_timeslot"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id"),
    )
    experiment_timeslot_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("experiment_timeslot.id"),
    )
    experiment_date: Mapped[date] = mapped_column(DATE, nullable=False, index=True)
    attendance_status: Mapped[ExperimentAttendanceStatusTypeEnum] = mapped_column(
        Enum(ExperimentAttendanceStatusTypeEnum),
        nullable=False,
        default=ExperimentAttendanceStatusTypeEnum.SCHEDULED,
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="experiment_participant_timeslots",
        uselist=False,
        lazy="selectin",
    )
    experiment_timeslot: Mapped["ExperimentTimeslot"] = relationship(
        "ExperimentTimeslot",
        back_populates="experiment_participant_timeslots",
        uselist=False,
        lazy="selectin",
    )


class ExperimentTimeslotRead(BaseModel):
    id: int = Field(..., description="ID")
    start_time: time = Field(..., description="Experiment start time")
    end_time: time = Field(..., description="Experiment end time")
    max_participants: int = Field(
        ..., description="Maximum number of exparticipants per session"
    )


class ExperimentProjectRead(BaseModel):
    id: int = Field(..., description="ID")
    title: str = Field(..., description="Title")
    description: str | None = Field(None, description="Description")
    is_public: bool = Field(..., description="Whether the project is public")
    start_date: date | None = Field(..., description="Experiment start date")
    end_date: date | None = Field(..., description="Experiment end date")
    excluded_dates: list[str] = Field(..., description="Experimental exclusion days")
    experiment_timeslots: list[ExperimentTimeslotRead] = Field(
        ..., description="Time information of experiment"
    )
    max_participants: int = Field(
        ..., description="Maximum number of experiment participants"
    )
    experiment_type: ExperimentTypeEnum = Field(...)
    location: str | None = Field(..., description="Experiment location")
    created_at: datetime = Field(..., description="Created datetime")
    updated_at: datetime = Field(..., description="Updated datetime")


class ExperimentParticipantTimeslotRead(BaseModel):
    id: int = Field(..., description="Participant ID")
    username: str = Field(..., description="Username")
    profile_color: str = Field(..., description="Profile color")
    experiment_date: date = Field(..., description="Experiment Date")
    start_time: time = Field(..., description="Experiment start time")
    end_time: time = Field(..., description="Experiment end time")
    attendance_status: ExperimentAttendanceStatusTypeEnum = Field(
        ..., description="Attendance Status"
    )
    created_at: datetime = Field(..., description="Created datetime")
    updated_at: datetime = Field(..., description="Updated datetime")
