from abc import ABC, abstractmethod

from app.auth.domain.vo import EmailVerificationType


class ExternalSystemPort(ABC):
    @abstractmethod
    async def send_email(
        self, email: str, code: str, verification_type: EmailVerificationType
    ) -> None:
        """Send email"""
