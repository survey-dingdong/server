from pydantic import BaseModel, EmailStr, Field, SecretStr


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Email")
    password: str = Field(..., description="Password")


class CreateUserRequest(BaseModel):
    email: EmailStr = Field(..., description="Email")
    password1: SecretStr = Field(..., description="Password1")
    password2: SecretStr = Field(..., description="Password2")
    username: str = Field(..., description="username")
