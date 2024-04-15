from pydantic import BaseModel, SecretStr


class CreateUserCommand(BaseModel):
    email: str
    password1: SecretStr
    password2: SecretStr
    nickname: str
