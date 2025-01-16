from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.user.domain.entity.user import User
from core.db import BaseWithInId

if TYPE_CHECKING:
    from app.project.domain.entity.experiment import ExperimentProject


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
        back_populates="workspaces",
        uselist=False,
        init=False,
        lazy="selectin",
    )

    experiment_projects: Mapped[list["ExperimentProject"]] = relationship(
        "ExperimentProject",
        back_populates="workspace",
        init=False,
        lazy="selectin",
    )

    @classmethod
    def create(cls, user_id: int, title: str, order_no: int) -> "Workspace":
        return cls(user_id=user_id, title=title, order_no=order_no)


class WorkspaceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID")
    title: str = Field(..., description="Title")
    order_no: int = Field(..., description="Order")
