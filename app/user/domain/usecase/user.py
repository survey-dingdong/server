from abc import ABC, abstractmethod

from pydantic import SecretStr

from app.user.application.dto import (
    CreateUserResponseDTO,
    GetUserListResponseDTO,
    GetUserResponseDTO,
    LoginResponseDTO,
    UpdateUserRequestDTO,
)
from app.user.domain.vo import LoginTypeEnum, OauthProviderTypeEnum


class UserUseCase(ABC):
    @abstractmethod
    async def is_email_available(self, email: str) -> bool:
        """Validate user email"""

    @abstractmethod
    async def get_user_list(self, page: int, size: int) -> list[GetUserListResponseDTO]:
        """Get user list"""

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> GetUserResponseDTO:
        """Get user"""

    @abstractmethod
    async def create_user(
        self,
        email: str,
        username: str,
        password: SecretStr,
    ) -> CreateUserResponseDTO:
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
    async def login(
        self, email: str, password: SecretStr, login_type: LoginTypeEnum
    ) -> LoginResponseDTO:
        """Login"""

    @abstractmethod
    async def oauth_login(
        self,
        email: str,
        username: str,
        provider: OauthProviderTypeEnum,
        oauth_id: str,
        login_type: LoginTypeEnum,
    ) -> LoginResponseDTO:
        """Oauth Login"""

    @abstractmethod
    async def change_password(
        self, user_id: int, old_password: SecretStr, new_password: SecretStr
    ) -> None:
        """Change password"""

    @abstractmethod
    async def reset_password(self, email: str, new_password: SecretStr) -> None:
        """Reset password"""
