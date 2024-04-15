from sqlalchemy import or_, select

from app.user.domain.entity.user import User
from app.user.domain.repository.user import UserRepo
from core.db.session import session


class UserSQLAlchemyRepo(UserRepo):
    async def get_users(self, page: int, size: int) -> list[User]:
        query = select(User).offset((page - 1) * size).limit(size)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_user_by_email_or_nickname(
        self, email: str, nickname: str
    ) -> User | None:
        stmt = await session.execute(
            select(User).where(or_(User.email == email, User.nickname == nickname)),
        )
        return stmt.scalars().first()

    async def get_user_by_id(self, user_id: int) -> User | None:
        query = await session.execute(select(User).where(User.id == user_id))
        return query.scalars().first()

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = await session.execute(select(User).where(User.email == email))
        return stmt.scalars().first()

    async def save(self, user: User) -> None:
        session.add(user)
