import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.server import app
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.user.application.exception import (
    DuplicateEmailOrusernameException,
    PasswordDoesNotMatchException,
    UserNotFoundException,
)
from core.helpers.auth import generate_hashed_password
from tests.support.constants import USER_ID_1_TOKEN
from tests.support.user_fixture import make_user

HEADERS = {"Authorization": f"Bearer {USER_ID_1_TOKEN}"}
BASE_URL = "http://test"


@pytest.mark.asyncio
async def test_get_users(session: AsyncSession):
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="survey-dingdong",
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
    assert sut[0] == {"id": 1, "email": "a@b.c", "username": "survey-dingdong"}


@pytest.mark.asyncio
async def test_get_user_me(session: AsyncSession):
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="survey-dingdong",
        is_admin=True,
    )
    session.add(user)
    await session.commit()

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/users/me", headers=HEADERS)

    # Then
    sut = response.json()
    assert sut == {"id": 1, "email": "a@b.c", "username": "survey-dingdong"}


@pytest.mark.asyncio
async def test_create_user_password_does_not_match(session: AsyncSession):
    # Given
    body = {
        "email": "survey@ding.dong",
        "password1": "Qwer1234!",
        "password2": "Qwer1234@",
        "username": "survey-dingdong",
    }
    exc = PasswordDoesNotMatchException

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
        username="survey-dingdong",
        is_admin=True,
    )
    session.add(user)
    await session.commit()

    body = {
        "email": "a@b.c",
        "password1": "Qwer1234!",
        "password2": "Qwer1234!",
        "username": "survey-dingdong",
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


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession):
    # Given
    email = "survey@ding.dong"
    username = "survey-dingdong"
    body = {
        "email": email,
        "password1": "Qwer1234!",
        "password2": "Qwer1234!",
        "username": username,
    }

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/users", headers=HEADERS, json=body)

    # Then
    assert response.json() == {"email": email, "username": username}

    user_repo = UserSQLAlchemyRepo()
    sut = await user_repo.get_user_by_email_or_username(username=username, email=email)
    assert sut is not None
    assert sut.email == email
    assert sut.username == username


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
        username="survey-dingdong",
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
