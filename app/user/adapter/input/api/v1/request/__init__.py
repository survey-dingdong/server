import re

from pydantic import BaseModel, EmailStr, SecretStr, field_validator


class CreateUserRequest(BaseModel):
    email: EmailStr
    password: SecretStr
    username: str

    @field_validator("password")
    @classmethod
    def check_password(cls, v: SecretStr) -> SecretStr:
        password_pattern = (
            "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[~!@#$%^&*_]).{8,20}$"
        )
        valid_password = re.match(password_pattern, v.get_secret_value())
        if valid_password is None:
            raise ValueError(
                "Please write a minimum of 8 characters and a maximum of 20 characters using a combination of uppercase and lowercase special characters."
            )
        return v


class UpdateUserRequest(BaseModel):
    username: str | None
    phone_num: str | None


class LoginRequest(BaseModel):
    email: EmailStr
    password: SecretStr


class OauthLoginRequest(BaseModel):
    email: EmailStr
    username: str
    oauth_id: str


class ChangePasswordRequest(BaseModel):
    old_password: SecretStr
    new_password: SecretStr
