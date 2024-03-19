from pydantic import BaseModel, Field


class GetWorkspaceListRepsonseDTO(BaseModel):
    id: int = Field(..., description="ID")
    title: str = Field(..., description="Title")
    order: int = Field(..., description="Order")


class CreateWorkspaceResponseDTO(BaseModel):
    id: int = Field(..., description="ID")
