from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base
from core.db.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.project.domain.entity.experiment import ExperimentProject


class Workspace(Base, TimestampMixin):
    __tablename__ = "workspace"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(20), nullable=False)
    order: Mapped[int] = mapped_column(Integer, autoincrement=True)

    experiment_projects: Mapped[list["ExperimentProject"]] = relationship(
        "ExperimentProject",
        back_populates="workspace",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @classmethod
    def create(cls, user_id: int, title: str) -> "Workspace":
        return cls(user_id=user_id, title=title)

    @classmethod
    def change_title(cls, title: str) -> None:
        cls.title = title

    @classmethod
    def change_order(cls, order: int) -> None:
        cls.order = order


class WorkspaceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID")
    title: str = Field(..., description="Title")
    order: int = Field(..., description="Order")
