from app.user.domain.entity.user import User, UserRead
from app.user.domain.repository.user import UserRepo


class UserRepositoryAdapter:
    def __init__(self, repository: UserRepo):
        self.repository = repository

    async def get_users(self, page: int, size: int) -> list[UserRead]:
        users = await self.repository.get_users(page=page, size=size)
        return [UserRead.model_validate(user) for user in users]

    async def get_user_by_email_or_nickname(
        self, email: str, nickname: str
    ) -> User | None:
        return await self.repository.get_user_by_email_or_nickname(
            email=email,
            nickname=nickname,
        )

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.repository.get_user_by_id(user_id=user_id)

    async def get_user_by_email(self, email: str) -> User | None:
        return await self.repository.get_user_by_email(email=email)

    async def save(self, user: User) -> None:
        await self.repository.save(user=user)
