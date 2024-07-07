from abc import ABC, abstractmethod

from app.user.domain.entity.user import User, UserOauth


class UserRepo(ABC):
    @abstractmethod
    async def get_users(self, page: int, size: int) -> list[User]:
        """Get user list"""

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None:
        """Get user by id"""

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        """Get user by email"""

    @abstractmethod
    async def get_user_oauth_by_id(
        self, user_id: int, oauth_id: str
    ) -> UserOauth | None:
        """Get user oauth by id"""

    @abstractmethod
    async def save(self, user: User | UserOauth, auto_flush: bool) -> User | UserOauth:
        """Save user"""
