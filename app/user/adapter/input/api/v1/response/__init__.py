from pydantic import BaseModel, Field


class GetUserListResponse(BaseModel):
    id: int = Field(..., description="ID")
    email: str = Field(..., description="Email")
    username: str = Field(..., description="username")


class CreateUserResponse(BaseModel):
    email: str = Field(..., description="Email")
    username: str = Field(..., description="username")


class LoginResponse(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
