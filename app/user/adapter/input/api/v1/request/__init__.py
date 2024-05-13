import re

from pydantic import BaseModel, EmailStr, Field, SecretStr, field_validator


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Email")
    password: str = Field(..., description="Password")


class CreateUserRequest(BaseModel):
    email: EmailStr = Field(..., description="Email")
    password1: SecretStr = Field(..., description="Password1")
    password2: SecretStr = Field(..., description="Password2")
    username: str = Field(..., description="username")

    @field_validator("password1", "password2")
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
