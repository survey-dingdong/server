from __future__ import annotations

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.user.domain.vo import OauthProviderTypeEnum
from core.db import BaseWithInId


class User(BaseWithInId):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(String(255), index=True)

    password: Mapped[str | None] = mapped_column(String(255), nullable=True)

    username: Mapped[str] = mapped_column(String(64))

    phone_num: Mapped[str | None] = mapped_column(String(20), init=False, nullable=True)

    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)


class UserOauth(BaseWithInId):
    __tablename__ = "user_oauth"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    user: Mapped[User] = relationship("User", init=False)

    oauth_id: Mapped[str] = mapped_column(String(255))

    provider: Mapped[OauthProviderTypeEnum] = mapped_column(Enum(OauthProviderTypeEnum))
