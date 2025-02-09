from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.user.domain.vo import OauthProviderTypeEnum
from core.db import BaseWithInId
from core.helpers.utils import get_random_color


class User(BaseWithInId):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(String(255), index=True)

    password: Mapped[str | None] = mapped_column(String(255), nullable=True)

    username: Mapped[str] = mapped_column(String(64))

    phone_num: Mapped[str | None] = mapped_column(String(20), init=False, nullable=True)

    profile_color: Mapped[str] = mapped_column(String(7))

    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    @classmethod
    def create(
        cls,
        *,
        email: str,
        username: str,
        password: str | None = None,
    ) -> "User":
        return cls(
            email=email,
            password=password,
            username=username,
            profile_color=get_random_color(),
        )


class UserOauth(BaseWithInId):
    __tablename__ = "user_oauth"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    user: Mapped[User] = relationship("User", init=False)

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
    profile_color: str = Field(default="#3F57FD", title="profile color")
    oauth_accounts: list[UserOauth] = Field(..., title="oauth accounts")
