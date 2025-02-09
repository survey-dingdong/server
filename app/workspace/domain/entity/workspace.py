from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.user.domain.entity.user import User
from core.db import BaseWithInId


class Workspace(BaseWithInId):
    __tablename__ = "workspace"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id"),
    )

    title: Mapped[str] = mapped_column(String(20))

    order_no: Mapped[int] = mapped_column(Integer)

    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["User"] = relationship(
        "User",
        uselist=False,
        init=False,
    )
