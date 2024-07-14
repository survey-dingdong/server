from __future__ import annotations

import random
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.user.domain.vo import OauthProviderTypeEnum
from core.db import Base
from core.db.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.project.domain.entity.experiment import ExperimentParticipantTimeslot
    from app.workspace.domain.entity.workspace import Workspace


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(64), nullable=False)
    phone_num: Mapped[str] = mapped_column(String(20), nullable=True)
    profile_color: Mapped[str] = mapped_column(String(7), nullable=False)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_deleted: Mapped[bool] = mapped_column(nullable=False, default=False)

    workspaces: Mapped[list["Workspace"]] = relationship(
        "Workspace", back_populates="user", lazy="selectin"
    )
    oauth_accounts: Mapped[list["UserOauth"]] = relationship(
        "UserOauth", back_populates="user", lazy="selectin"
    )
    experiment_participant_timeslots: Mapped[
        "ExperimentParticipantTimeslot"
    ] = relationship(
        "ExperimentParticipantTimeslot", back_populates="user", lazy="selectin"
    )

    @staticmethod
    def random_color() -> str:
        colors = ["#3F57FD", "#DB5654", "#613EE2", "#FD3F78", "#F08F1D", "#24A29A"]
        return random.choice(colors)

    @classmethod
    def create(
        cls, *, email: str, username: str, password: str | None = None
    ) -> "User":
        return cls(
            email=email,
            password=password,
            username=username,
            profile_color=cls.random_color(),
        )


class UserOauth(Base, TimestampMixin):
    __tablename__ = "user_oauth"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    user: Mapped[User] = relationship(
        "User", back_populates="oauth_accounts", uselist=False
    )
    oauth_id: Mapped[str] = mapped_column(String(255), nullable=False)
    provider: Mapped[OauthProviderTypeEnum] = mapped_column(
        Enum(OauthProviderTypeEnum), nullable=False
    )

    @classmethod
    def create(
        cls, *, user_id: int, oauth_id: str, provider: OauthProviderTypeEnum
    ) -> "UserOauth":
        return cls(
            user_id=user_id,
            oauth_id=oauth_id,
            provider=provider,
        )


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    id: int = Field(..., title="USER ID")
    email: str = Field(..., title="Email")
    username: str = Field(..., title="username")
    profile_color: str = Field(..., title="profile color")
    oauth_accounts: list[UserOauth] = Field(..., title="oauth accounts")
