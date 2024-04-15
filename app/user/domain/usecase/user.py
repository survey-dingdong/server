from abc import ABC, abstractmethod

from app.user.application.dto import LoginResponseDTO
from app.user.domain.command import CreateUserCommand
from app.user.domain.entity.user import User


class UserUseCase(ABC):
    @abstractmethod
    async def get_user_list(self, page: int, size: int) -> list[User]:
        """Get user list"""

    @abstractmethod
    async def create_user(self, command: CreateUserCommand) -> None:
        """Create User"""

    @abstractmethod
    async def is_admin(self, user_id: int) -> bool:
        """Is admin"""

    @abstractmethod
    async def login(self, email: str, password: str) -> LoginResponseDTO:
        """Login"""
