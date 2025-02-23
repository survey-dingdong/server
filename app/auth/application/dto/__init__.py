from pydantic import BaseModel


class RefreshTokenResponseDTO(BaseModel):
    access_token: str
    refresh_token: str


class ValidateEmailResponseDTO(BaseModel):
    availability: bool
