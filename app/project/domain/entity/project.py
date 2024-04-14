from datetime import datetime

from pydantic import BaseModel, Field
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.db.mixins import TimestampMixin


class Project(TimestampMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    workspace_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("workspace.id"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(String(512))
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    joined_participants: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_participants: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


class ProjectRead(BaseModel):
    id: int = Field(..., description="ID")
    workspace_id: int = Field(..., description="Workspace ID")
    title: str = Field(..., description="Title")
    description: str | None = Field(None, description="Description")
    is_public: bool = Field(..., description="Whether the project is public")
    joined_participants: int = Field(
        ..., description="Number of experiment participants"
    )
    max_participants: int = Field(
        ..., description="Maximum number of experiment participants"
    )
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)
