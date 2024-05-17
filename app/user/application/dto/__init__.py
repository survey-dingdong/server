from pydantic import BaseModel, Field


class CreateUserResponseDTO(BaseModel):
    token: str = Field(..., description="Token")


class LoginResponseDTO(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
