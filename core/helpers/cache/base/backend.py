from abc import ABC, abstractmethod
from typing import Any


class BaseBackend(ABC):
    @abstractmethod
    async def get(self, *, key: str) -> Any:
        """Get"""

    @abstractmethod
    async def set(self, *, response: Any, key: str, ttl: int = 60) -> None:
        """Set"""

    @abstractmethod
    async def delete(self, *, key: str) -> None:
        """Delete"""

    @abstractmethod
    async def delete_startswith(self, *, value: str) -> None:
        """Delete starts with"""

    @abstractmethod
    async def store_login_session(
        self, *, user_id: int, login_type: str, token: str
    ) -> None:
        """Store login session"""

    @abstractmethod
    async def validate_login_session(
        self, *, user_id: int, login_type: str, token: str
    ) -> bool:
        """Validate login session"""

    @abstractmethod
    async def store_refresh_token(self, *, user_id: int, value: str) -> None:
        """Store refresh token"""

    @abstractmethod
    async def get_refresh_token(self, *, user_id: int) -> Any:
        """Get refresh token"""
