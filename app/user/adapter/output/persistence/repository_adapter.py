from app.user.application.dto import UserOauthResponseDTO
from app.user.domain.entity.user import User, UserOauth
from app.user.domain.repository.user import UserRepo


class UserRepositoryAdapter:
    def __init__(self, repository: UserRepo):
        self.repository = repository

    async def get_user_oauth_accounts(
        self, user_ids: list[int]
    ) -> dict[int, list[UserOauthResponseDTO]]:
        return await self.repository.get_user_oauth_accounts(user_ids=user_ids)

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

    async def add(self, user: User | UserOauth, auto_flush: bool = False) -> User:
        return await self.repository.add(user=user, auto_flush=auto_flush)
