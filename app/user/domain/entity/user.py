from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from core.db.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.project.domain.entity.experiment import ExperimentParticipantTimeslot


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(64), nullable=False)
    phone_num: Mapped[str] = mapped_column(String(20), nullable=True, unique=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    experiment_participant_timeslots: Mapped[
        "ExperimentParticipantTimeslot"
    ] = relationship(
        "ExperimentParticipantTimeslot", back_populates="user", lazy="selectin"
    )

    @classmethod
    def create(cls, *, email: str, password: str, username: str) -> "User":
        return cls(
            email=email,
            password=password,
            username=username,
            is_admin=False,
        )


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="USER ID")
    email: str = Field(..., title="Email")
    username: str = Field(..., title="username")
