from abc import ABC, abstractmethod


class ExternalSystemPort(ABC):
    @abstractmethod
    async def send_email(self, email: str, code: str) -> None:
        """Send email"""
