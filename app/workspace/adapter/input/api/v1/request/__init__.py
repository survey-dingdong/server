from pydantic import BaseModel, Field


class CreateWorkspaceRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=20, description="Title")


class UpdateWorkspaceRequest(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=20, description="Title")
    order_no: int | None = Field(None, ge=1, description="New order no")
