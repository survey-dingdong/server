from abc import ABC, abstractmethod

from pydantic import SecretStr

from app.user.application.dto import CreateUserResponseDTO, LoginResponseDTO
from app.user.domain.command import CreateUserCommand
from app.user.domain.entity.user import User


class UserUseCase(ABC):
    @abstractmethod
    async def get_user_list(self, page: int, size: int) -> list[User]:
        """Get user list"""

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User:
        """Get user list"""

    @abstractmethod
    async def create_user(self, command: CreateUserCommand) -> CreateUserResponseDTO:
        """Create User"""

    @abstractmethod
    async def is_admin(self, user_id: int) -> bool:
        """Is admin"""

    @abstractmethod
    async def login(self, email: str, password: SecretStr) -> LoginResponseDTO:
        """Login"""

    @abstractmethod
    async def change_password(
        self, user_id: int, old_password: SecretStr, new_password: SecretStr
    ) -> None:
        """Change password"""
