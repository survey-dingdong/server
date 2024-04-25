from pydantic import BaseModel, Field


class CreateWorkspaceRequest(BaseModel):
    title: str = Field(..., description="Title")


class UpdateWorkspaceRequest(BaseModel):
    title: str | None = Field(None, description="Title")
    order_no: int | None = Field(None, description="New order no")
