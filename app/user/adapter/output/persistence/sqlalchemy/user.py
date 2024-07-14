from sqlalchemy import and_, select

from app.user.domain.entity.user import User, UserOauth
from app.user.domain.repository.user import UserRepo
from core.db.session import session


class UserSQLAlchemyRepo(UserRepo):
    async def get_users(self, page: int, size: int) -> list[User]:
        query = select(User).offset((page - 1) * size).limit(size)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_user_by_id(self, user_id: int) -> User | None:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> User | None:
        result = await session.execute(
            select(User).where(
                and_(
                    User.email == email,
                    ~User.is_deleted,
                )
            )
        )
        return result.scalars().first()

    async def get_user_by_oauth_id(
        self, user_id: int, oauth_id: str
    ) -> UserOauth | None:
        result = await session.execute(
            select(UserOauth)
            .join(User)
            .where(
                and_(
                    UserOauth.user_id == user_id,
                    UserOauth.oauth_id == oauth_id,
                    ~User.is_deleted,
                )
            )
        )
        return result.scalars().first()

    async def save(self, user: User | UserOauth, auto_flush: bool = False) -> User:
        session.add(user)
        if auto_flush:
            await session.flush()
        return user
