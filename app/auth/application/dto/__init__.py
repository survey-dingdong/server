from pydantic import BaseModel


class RefreshTokenResponseDTO(BaseModel):
    token: str
    refresh_token: str


class ValidateEmailResponseDTO(BaseModel):
    availability: bool
