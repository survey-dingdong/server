from pydantic import BaseModel, Field


class UserOauthResponse(BaseModel):
    id: int = Field(..., description="ID")
    oauth_id: str = Field(..., description="Oauth ID")
    provider: str = Field(..., description="Provider")


class GetUserListResponse(BaseModel):
    id: int = Field(..., description="ID")
    email: str = Field(..., description="Email")
    username: str = Field(..., description="username")
    profile_color: str = Field(..., description="profile color")
    oauth_accounts: list[UserOauthResponse] = Field(..., description="oauth accounts")


class CreateUserResponse(BaseModel):
    token: str = Field(..., description="Token")


class LoginResponse(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")
