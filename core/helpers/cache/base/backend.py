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
