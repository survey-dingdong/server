from collections import defaultdict
from typing import cast

from sqlalchemy import and_, select

from app.user.application.dto import UserOauthResponseDTO
from app.user.domain.entity.user import User, UserOauth
from app.user.domain.repository.user import UserRepo
from core.db.session import session


class UserSQLAlchemyRepo(UserRepo):
    async def get_user_oauth_accounts(
        self, user_ids: list[int]
    ) -> dict[int, list[UserOauthResponseDTO]]:
        user_oauths = (
            (
                await session.execute(
                    select(UserOauth).where(UserOauth.user_id.in_(user_ids))
                )
            )
            .scalars()
            .all()
        )

        user_id_to_oauth_accounts = defaultdict(list)
        for user_oauth in user_oauths:
            user_id_to_oauth_accounts[user_oauth.user_id].append(
                UserOauthResponseDTO(
                    id=user_oauth.id,
                    oauth_id=user_oauth.oauth_id,
                    provider=user_oauth.provider,
                )
            )

        return user_id_to_oauth_accounts

    async def get_users(self, page: int, size: int) -> list[User]:
        users = (
            (await session.execute(select(User).offset((page - 1) * size).limit(size)))
            .scalars()
            .all()
        )

        return cast(list[User], users)

    async def get_user_by_id(self, user_id: int) -> User | None:
        user = (
            await session.execute(select(User).where(User.id == user_id))
        ).scalar_one_or_none()

        return user

    async def get_user_by_email(self, email: str) -> User | None:
        result = await session.execute(
            select(User).where(
                and_(
                    User.email == email,
                    ~User.is_deleted,
                )
            )
        )
        return result.scalar_one_or_none()

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
        return result.scalar_one_or_none()

    async def add(self, user: User | UserOauth, auto_flush: bool = False) -> User:
        session.add(user)
        if auto_flush:
            await session.flush()
        return cast(User, user)
