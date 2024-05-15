from pydantic import BaseModel, SecretStr


class CreateUserCommand(BaseModel):
    email: str
    password: SecretStr
    username: str
