from pydantic import BaseModel, Field


class GetWorkspaceRepsonseDTO(BaseModel):
    id: int = Field(..., description="ID")
    title: str = Field(..., description="Title")
    order_no: int = Field(..., description="Order")


class CreateWorkspaceResponseDTO(BaseModel):
    id: int = Field(..., description="ID")
