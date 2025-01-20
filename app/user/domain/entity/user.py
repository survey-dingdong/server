from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.user.domain.vo import OauthProviderTypeEnum, UserRoleEnum
from core.db import BaseWithInId
from core.helpers.utils import get_random_color

if TYPE_CHECKING:
    from app.project.domain.entity.experiment import ExperimentParticipantTimeslot
    from app.workspace.domain.entity.workspace import Workspace


class User(BaseWithInId):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(String(255), index=True)

    password: Mapped[str | None] = mapped_column(String(255), nullable=True)

    username: Mapped[str] = mapped_column(String(64))

    phone_num: Mapped[str | None] = mapped_column(String(20), init=False, nullable=True)

    profile_color: Mapped[str] = mapped_column(String(7))

    role: Mapped[UserRoleEnum] = mapped_column(Enum(UserRoleEnum))

    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    workspaces: Mapped[list["Workspace"]] = relationship(
        "Workspace", back_populates="user", init=False, lazy="selectin"
    )

    oauth_accounts: Mapped[list["UserOauth"]] = relationship(
        "UserOauth", back_populates="user", init=False, lazy="selectin"
    )

    experiment_participant_timeslots: Mapped[
        "ExperimentParticipantTimeslot"
    ] = relationship(
        "ExperimentParticipantTimeslot",
        back_populates="user",
        init=False,
        lazy="selectin",
    )

    @classmethod
    def create(
        cls,
        *,
        email: str,
        username: str,
        password: str | None = None,
        role: UserRoleEnum = UserRoleEnum.Researcher,
    ) -> "User":
        return cls(
            email=email,
            password=password,
            username=username,
            role=role,
            profile_color=get_random_color(),
        )


class UserOauth(BaseWithInId):
    __tablename__ = "user_oauth"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    user: Mapped[User] = relationship(
        "User", back_populates="oauth_accounts", init=False
    )

    oauth_id: Mapped[str] = mapped_column(String(255))

    provider: Mapped[OauthProviderTypeEnum] = mapped_column(Enum(OauthProviderTypeEnum))

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
