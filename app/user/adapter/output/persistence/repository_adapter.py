from app.user.domain.entity.user import User, UserOauth
from app.user.domain.repository.user import UserRepo


class UserRepositoryAdapter:
    def __init__(self, repository: UserRepo):
        self.repository = repository

    async def get_users(self, page: int, size: int) -> list[User]:
        return await self.repository.get_users(page=page, size=size)

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.repository.get_user_by_id(user_id=user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.repository.get_user_by_email(email=email)

    async def get_user_by_oauth_id(
        self, user_id: int, oauth_id: str
    ) -> UserOauth | None:
        return await self.repository.get_user_by_oauth_id(
            user_id=user_id, oauth_id=oauth_id
        )

    async def save(
        self, user: User | UserOauth, auto_flush: bool = False
    ) -> User | UserOauth:
        return await self.repository.save(user=user, auto_flush=auto_flush)
