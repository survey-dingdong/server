from pydantic import BaseModel, Field


class CreateProjectResponseDTO(BaseModel):
    id: int = Field(..., description="ID")
