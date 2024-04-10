from pydantic import BaseModel, Field


class WorkspaceResponse(BaseModel):
    id: int = Field(..., description="ID")
    title: str = Field(..., description="Title")
    order: int = Field(..., description="Order")


class CreateWorkspaceResponse(BaseModel):
    id: int = Field(..., description="ID")


class UpdateWorkspaceRepsonse(BaseModel):
    id: int = Field(..., description="ID")
    title: str = Field(..., description="Title")
    order: int = Field(..., description="Order")
