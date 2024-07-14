import pytest
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
from core.helpers.auth import generate_hashed_password
from core.helpers.cache import RedisBackend
from tests.support.constants import USER_ID_1_TOKEN
from tests.support.user_fixture import make_user

HEADERS = {"Authorization": f"Bearer {USER_ID_1_TOKEN}"}
BASE_URL = "http://test"

redis_backend = RedisBackend()


@pytest.mark.asyncio
async def test_get_users(session: AsyncSession):
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
        response = await client.get("/users", headers=HEADERS)

    # Then
    sut = response.json()
    assert len(sut) == 1
    assert sut[0] == {
        "id": 1,
        "email": "a@b.c",
        "username": "dingdong-survey",
        "profile_color": "#3F57FD",
        "oauth_accounts": [],
    }


@pytest.mark.asyncio
async def test_get_user_me(session: AsyncSession):
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
        response = await client.get("/users/me", headers=HEADERS)

    # Then
    sut = response.json()
    assert sut == {
        "id": 1,
        "email": "a@b.c",
        "username": "dingdong-survey",
        "profile_color": "#3F57FD",
        "oauth_accounts": [],
    }


@pytest.mark.asyncio
async def test_create_user_unauthorized(session: AsyncSession):
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
        "password": "Qwer1234!",
        "username": "dingdong-survey",
    }
    exc = UnauthorizedAccessException

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/users", headers=HEADERS, json=body)

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_create_user_duplicated_user(session: AsyncSession):
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )
    session.add(user)
    await session.commit()

    signup_redis_key = f"dingdong-survey::{EmailVerificationType.SIGNUP}::{user.email}"
    await redis_backend.set(response="signup_code", key=signup_redis_key)

    body = {
        "email": "a@b.c",
        "password": "Qwer1234!",
        "username": "dingdong-survey",
    }
    exc = DuplicateEmailOrusernameException

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/users", headers=HEADERS, json=body)

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }
    await redis_backend.delete(key=signup_redis_key)


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession):
    # Given
    email = "survey@ding.dong"
    username = "dingdong-survey"
    body = {
        "email": email,
        "password": "Qwer1234!",
        "username": username,
    }
    signup_redis_key = f"dingdong-survey::{EmailVerificationType.SIGNUP}::{email}"
    await redis_backend.set(response="signup_code", key=signup_redis_key)

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        await client.post("/users", headers=HEADERS, json=body)

    # Then
    user_repo = UserSQLAlchemyRepo()
    sut = await user_repo.get_user_by_email(email=email)
    assert sut is not None
    assert sut.email == email
    assert sut.username == username

    await redis_backend.delete(key=signup_redis_key)


@pytest.mark.asyncio
async def test_login_user_not_found(session: AsyncSession):
    # Given
    email = "survey@ding.dong"
    password = "password"
    body = {"email": email, "password": password}
    exc = UserNotFoundException

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/users/login", headers=HEADERS, json=body)

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_login(session: AsyncSession):
    # Given
    email = "survey@ding.dong"
    password = "password"
    user = make_user(
        password=generate_hashed_password(password=password),
        email=email,
        username="dingdong-survey",
        is_admin=True,
    )
    session.add(user)
    await session.commit()

    body = {"email": email, "password": password}

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/users/login", headers=HEADERS, json=body)

    # Then
    sut = response.json()
    assert "token" in sut
    assert "refresh_token" in sut
