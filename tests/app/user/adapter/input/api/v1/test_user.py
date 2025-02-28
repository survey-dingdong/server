import pytest
from dependency_injector import providers
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.domain.vo import EmailVerificationType
from app.server import app
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.user.application.exception import (
    DuplicateEmailOrusernameException,
    UnauthorizedAccessException,
    UserNotFoundException,
)
from app.user.container import UserContainer
from app.user.domain.vo import LoginTypeEnum
from core.constants import (
    EMAIL_VERIFICATION_PREFIX,
    LOGIN_SESSION_PREFIX,
    REFRESH_TOKEN_PREFIX,
)
from core.helpers.cache.redis_backend import RedisBackend
from tests.support.user_fixture import make_user

BASE_URL = "http://test"


@pytest.mark.asyncio
async def test_get_users(session: AsyncSession, access_token: str) -> None:
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )
    session.add(user)
    await session.commit()

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/users",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    # Then
    sut = response.json()
    assert len(sut) == 1
    assert sut[0] == {
        "id": 1,
        "email": "a@b.c",
        "username": "dingdong-survey",
        "is_admin": True,
        "is_deleted": False,
        "oauth_accounts": [],
    }


@pytest.mark.asyncio
async def test_get_user_me(session: AsyncSession, access_token: str) -> None:
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )
    session.add(user)
    await session.commit()

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    # Then
    sut = response.json()
    assert sut == {
        "id": 1,
        "email": "a@b.c",
        "username": "dingdong-survey",
        "profile_color": sut["profile_color"],
        "oauth_accounts": [],
    }


@pytest.mark.asyncio
async def test_create_user_unauthorized(
    session: AsyncSession, access_token: str, redis_backend: RedisBackend
) -> None:
    # Given
    container = UserContainer()
    container.redis_backend.override(providers.Object(redis_backend))

    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )
    session.add(user)
    await session.commit()

    body = {
        "email": "a@b.c",
        "username": "dingdong-survey",
        "password": "Qwer1234!",
    }
    exc = UnauthorizedAccessException

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/users", headers={"Authorization": f"Bearer {access_token}"}, json=body
        )

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_create_user_duplicated_user(
    session: AsyncSession, access_token: str, redis_backend: RedisBackend
) -> None:
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )
    session.add(user)
    await session.commit()

    signup_redis_key = f"{EMAIL_VERIFICATION_PREFIX}::{EmailVerificationType.SIGNUP}::email::{user.email}"
    await redis_backend.set(response="signup_code", key=signup_redis_key)

    body = {
        "email": "a@b.c",
        "username": "dingdong-survey",
        "password": "Qwer1234!",
    }
    exc = DuplicateEmailOrusernameException

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/users", headers={"Authorization": f"Bearer {access_token}"}, json=body
        )

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }
    await redis_backend.delete(key=signup_redis_key)


@pytest.mark.asyncio
async def test_create_user(access_token: str, redis_backend: RedisBackend) -> None:
    # Given
    email = "survey@ding.dong"
    username = "dingdong-survey"
    body = {
        "email": email,
        "username": username,
        "password": "Qwer1234!",
    }
    signup_redis_key = (
        f"{EMAIL_VERIFICATION_PREFIX}::{EmailVerificationType.SIGNUP}::email::{email}"
    )
    await redis_backend.set(response="signup_code", key=signup_redis_key)

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post(
            "/users", headers={"Authorization": f"Bearer {access_token}"}, json=body
        )

    # Then
    user_repo = UserSQLAlchemyRepo()
    sut = await user_repo.get_user_by_email(email=email)
    assert sut is not None
    assert sut.email == email
    assert sut.username == username

    await redis_backend.delete(key=signup_redis_key)


@pytest.mark.asyncio
async def test_login_user_not_found(access_token: str) -> None:
    # Given
    email = "survey2@ding.dong"
    password = "password"
    params = {"login_type": LoginTypeEnum.Web}
    body = {"email": email, "password": password}
    exc = UserNotFoundException

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/users/login",
            headers={"Authorization": f"Bearer {access_token}"},
            params=params,
            json=body,
        )

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_login(
    session: AsyncSession, access_token: str, redis_backend: RedisBackend
) -> None:
    # Given
    email = "survey2@ding.dong"
    password = "password"
    user = make_user(
        id=2,
        password=password,
        email=email,
        username="dingdong-survey",
        is_admin=True,
    )
    session.add(user)
    await session.commit()

    params = {"login_type": LoginTypeEnum.Web}
    body = {"email": email, "password": password}

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/users/login",
            headers={"Authorization": f"Bearer {access_token}"},
            params=params,
            json=body,
        )

    login_session_key = f"{LOGIN_SESSION_PREFIX}::{LoginTypeEnum.Web}::user::{user.id}"
    await redis_backend.delete(key=login_session_key)

    refresh_token_key = f"{REFRESH_TOKEN_PREFIX}::user::{user.id}"
    await redis_backend.delete(key=refresh_token_key)

    # Then
    sut = response.json()
    assert "access_token" in sut
    assert "refresh_token" in sut
