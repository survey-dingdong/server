from pydantic import BaseModel, Field


class GetUserListResponseDTO(BaseModel):
    id: int = Field(..., description="ID")
    email: str = Field(..., description="Email")
    username: str = Field(..., description="username")


class CreateUserRequestDTO(BaseModel):
    email: str = Field(..., description="Email")
    password1: str = Field(..., description="Password1")
    password2: str = Field(..., description="Password2")
    username: str = Field(..., description="username")


class CreateUserResponseDTO(BaseModel):
    email: str = Field(..., description="Email")
    username: str = Field(..., description="username")


class LoginResponseDTO(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
