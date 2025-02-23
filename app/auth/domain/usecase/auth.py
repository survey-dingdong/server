from abc import ABC, abstractmethod

from app.auth.application.dto import RefreshTokenResponseDTO
from app.auth.domain.vo import EmailVerificationType
from app.user.domain.vo import LoginTypeEnum


class AuthUseCase(ABC):
    @abstractmethod
    async def refresh_access_token(
        self,
        access_token: str,
        refresh_token: str,
        login_type: LoginTypeEnum,
    ) -> RefreshTokenResponseDTO:
        """Refresh access token"""

    @abstractmethod
    async def send_verification_email(
        self, email: str, verification_type: EmailVerificationType
    ) -> None:
        """Send email"""

    @abstractmethod
    async def validate_verification_email(
        self, email: str, code: str, verification_type: EmailVerificationType
    ) -> None:
        """Verify email"""
