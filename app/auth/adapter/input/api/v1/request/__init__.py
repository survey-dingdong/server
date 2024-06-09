from pydantic import BaseModel, EmailStr, Field


class RefreshTokenRequest(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")


class EmailVerificationRequest(BaseModel):
    email: EmailStr = Field(..., description="Email")


class VerifyEmailRequest(BaseModel):
    email: EmailStr = Field(..., description="Email")
    code: str = Field(..., description="Code")
