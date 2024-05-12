from sqlalchemy import or_, select

from app.user.domain.entity.user import User
from app.user.domain.repository.user import UserRepo
from core.db.session import session


class UserSQLAlchemyRepo(UserRepo):
    async def get_users(self, page: int, size: int) -> list[User]:
        query = select(User).offset((page - 1) * size).limit(size)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_user_by_email_or_username(
        self, email: str, username: str
    ) -> User | None:
        result = await session.execute(
            select(User).where(or_(User.email == email, User.username == username)),
        )
        return result.scalars().first()

    async def get_user_by_id(self, user_id: int) -> User | None:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> User | None:
        result = await session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def save(self, user: User) -> None:
        session.add(user)
