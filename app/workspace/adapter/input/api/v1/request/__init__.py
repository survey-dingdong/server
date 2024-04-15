from pydantic import BaseModel, Field


class CreateWorkspaceRequest(BaseModel):
    title: str = Field(..., description="Title")


class UpdateWorkspaceRequest(BaseModel):
    title: str | None = Field(None, description="Title")
    new_order: int | None = Field(None, description="New order no")
