from pydantic import BaseModel, Field

from core.helpers.utils import get_random_color


class UserOauthResponseDTO(BaseModel):
    id: int
    oauth_id: str
    provider: str


class GetUserListResponseDTO(BaseModel):
    id: int
    email: str
    username: str
    is_admin: bool
    is_deleted: bool
    oauth_accounts: list[UserOauthResponseDTO]


class GetUserResponseDTO(BaseModel):
    id: int
    email: str
    username: str
    profile_color: str = Field(default_factory=lambda: get_random_color())
    oauth_accounts: list[UserOauthResponseDTO]


class CreateUserResponseDTO(BaseModel):
    token: str


class UpdateUserRequestDTO(BaseModel):
    username: str | None
    phone_num: str | None


class LoginResponseDTO(BaseModel):
    token: str
    refresh_token: str
