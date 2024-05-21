from pydantic import BaseModel, Field


class CreateUserResponseDTO(BaseModel):
    token: str = Field(..., description="Token")


class UpdateUserRequestDTO(BaseModel):
    username: str | None
    phone_num: str | None


class LoginResponseDTO(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
