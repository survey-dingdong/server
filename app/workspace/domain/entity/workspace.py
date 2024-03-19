from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base
from core.db.mixins import TimestampMixin


class Workspace(Base, TimestampMixin):
    __tablename__ = "workspace"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(20), nullable=False)
    order: Mapped[int] = mapped_column(Integer, autoincrement=True)

    @classmethod
    def create(cls, user_id: int, title: str) -> "Workspace":
        return cls(user_id=user_id, title=title)


class WorkspaceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="ID")
    title: str = Field(..., description="Title")
