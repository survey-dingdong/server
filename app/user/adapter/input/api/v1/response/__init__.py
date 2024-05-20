from pydantic import BaseModel, Field


class GetUserListResponse(BaseModel):
    id: int = Field(..., description="ID")
    email: str = Field(..., description="Email")
    username: str = Field(..., description="username")


class CreateUserResponse(BaseModel):
    token: str = Field(..., description="Token")


class ValidateEmailResponse(BaseModel):
    availability: bool = Field(..., description="Email Availability")


class LoginResponse(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
