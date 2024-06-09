from abc import ABC, abstractmethod

from app.auth.application.dto import RefreshTokenResponseDTO
from app.auth.domain.vo import EmailVerificationType


class AuthUseCase(ABC):
    @abstractmethod
    async def create_refresh_token(
        self,
        token: str,
        refresh_token: str,
    ) -> RefreshTokenResponseDTO:
        """Create refresh token"""

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
