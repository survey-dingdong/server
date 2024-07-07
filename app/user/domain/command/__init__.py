from pydantic import BaseModel, SecretStr

from app.user.domain.vo import OauthProviderTypeEnum


class CreateUserCommand(BaseModel):
    email: str
    password: SecretStr
    username: str


class UserOauthCommand(BaseModel):
    email: str
    username: str
    provider: OauthProviderTypeEnum
    oauth_id: str
