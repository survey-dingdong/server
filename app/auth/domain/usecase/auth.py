from abc import ABC, abstractmethod

from app.auth.application.dto import RefreshTokenResponseDTO


class AuthUseCase(ABC):
    @abstractmethod
    async def create_refresh_token(
        self,
        token: str,
        refresh_token: str,
    ) -> RefreshTokenResponseDTO:
        """Create refresh token"""

    @abstractmethod
    async def send_email(self, email: str) -> None:
        """Send email"""
