from abc import ABC, abstractmethod

from pydantic import SecretStr

from app.user.application.dto import (
    CreateUserResponseDTO,
    LoginResponseDTO,
    UpdateUserRequestDTO,
)
from app.user.domain.command import CreateUserCommand, UserOauthCommand
from app.user.domain.entity.user import User


class UserUseCase(ABC):
    @abstractmethod
    async def is_email_available(self, email: str) -> bool:
        """Validate user email"""

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
    async def update_user(self, user_id: int, user_dto: UpdateUserRequestDTO) -> None:
        """Update User"""

    @abstractmethod
    async def delete_user(self, user_id: int) -> None:
        """Delete User"""

    @abstractmethod
    async def is_admin(self, user_id: int) -> bool:
        """Is admin"""

    @abstractmethod
    async def login(self, email: str, password: SecretStr) -> LoginResponseDTO:
        """Login"""

    @abstractmethod
    async def oauth_login(self, command: UserOauthCommand) -> LoginResponseDTO:
        """Oauth Login"""

    @abstractmethod
    async def change_password(
        self, user_id: int, old_password: SecretStr, new_password: SecretStr
    ) -> None:
        """Change password"""

    @abstractmethod
    async def reset_password(self, email: str, new_password: SecretStr) -> None:
        """Reset password"""
