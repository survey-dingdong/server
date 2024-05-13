from unittest.mock import AsyncMock

import pytest

from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.application.exception import (
    DuplicateEmailOrusernameException,
    PasswordDoesNotMatchException,
    UserNotFoundException,
)
from app.user.application.service.user import UserService
from app.user.domain.command import CreateUserCommand
from app.user.domain.entity.user import UserRead
from core.helpers.auth import generate_hashed_password
from core.helpers.cache import RedisBackend
from core.helpers.token import TokenHelper
from tests.support.user_fixture import make_user

repository_mock = AsyncMock(spec=UserRepositoryAdapter)
user_service = UserService(repository=repository_mock)

redis_backend = RedisBackend()


@pytest.mark.asyncio
async def test_get_user_list():
    # Given
    page = 1
    size = 10
    user = UserRead(id=1, email="survey@ding.dong", username="survey-dingdong")
    repository_mock.get_users.return_value = [user]
    user_service.repository = repository_mock

    # When
    sut = await user_service.get_user_list(page=page, size=size)

    # Then
    assert len(sut) == 1
    result = sut[0]

    assert result.email == user.email
    assert result.username == user.username
    user_service.repository.get_users.assert_awaited_once_with(page=page, size=size)


@pytest.mark.asyncio
async def test_get_user_me_not_exist():
    # Given
    repository_mock.get_user_by_id.return_value = None
    user_service.repository = repository_mock

    # When, Then
    with pytest.raises(UserNotFoundException):
        await user_service.get_user_by_id(user_id=1)


@pytest.mark.asyncio
async def test_get_user_me():
    # Given
    user = UserRead(id=1, email="survey@ding.dong", username="survey-dingdong")
    repository_mock.get_user_by_id.return_value = user
    user_service.repository = repository_mock

    # When
    sut = await user_service.get_user_by_id(user_id=user.id)

    # Then
    assert sut.email == user.email
    assert sut.username == user.username


@pytest.mark.asyncio
async def test_create_user_password_does_not_match():
    # Given
    command = CreateUserCommand(
        email="survey@ding.dong",
        password1="Qwer1234!",
        password2="Qwer1234@",
        username="survey-dingdong",
    )

    # When, Then
    with pytest.raises(PasswordDoesNotMatchException):
        await user_service.create_user(command=command)


@pytest.mark.asyncio
async def test_create_user_duplicated():
    # Given
    command = CreateUserCommand(
        email="survey@ding.dong",
        password1="Qwer1234!",
        password2="Qwer1234!",
        username="survey-dingdong",
    )
    user = make_user(
        password="password",
        email="survey@ding.dong",
        username="survey-dingdong",
        is_admin=False,
    )
    repository_mock.get_user_by_email_or_username.return_value = user
    user_service.repository = repository_mock

    # When, Then
    with pytest.raises(DuplicateEmailOrusernameException):
        await user_service.create_user(command=command)


@pytest.mark.asyncio
async def test_create_user():
    # Given
    command = CreateUserCommand(
        email="survey@ding.dong",
        password1="Qwer1234!",
        password2="Qwer1234!",
        username="survey-dingdong",
    )
    repository_mock.get_user_by_email_or_username.return_value = None
    user_service.repository = repository_mock

    # When
    await user_service.create_user(command=command)

    # Then
    repository_mock.save.assert_awaited_once()


@pytest.mark.asyncio
async def test_is_admin_user_not_exist():
    # Given
    repository_mock.get_user_by_id.return_value = None
    user_service.repository = repository_mock

    # When
    sut = await user_service.is_admin(user_id=1)

    # Then
    assert sut is False


@pytest.mark.asyncio
async def test_is_admin_user_is_not_admin():
    # Given
    user = make_user(
        password="password",
        email="survey@ding.dong",
        username="survey-dingdong",
        is_admin=False,
    )
    repository_mock.get_user_by_id.return_value = user
    user_service.repository = repository_mock

    # When
    sut = await user_service.is_admin(user_id=user.id)

    # Then
    assert sut is False


@pytest.mark.asyncio
async def test_is_admin():
    # Given
    user = make_user(
        password="password",
        email="survey@ding.dong",
        username="survey-dingdong",
        is_admin=True,
    )
    repository_mock.get_user_by_id.return_value = user
    user_service.repository = repository_mock

    # When
    sut = await user_service.is_admin(user_id=user.id)

    # Then
    assert sut is True


@pytest.mark.asyncio
async def test_login_user_not_exist():
    # Given
    repository_mock.get_user_by_email.return_value = None
    user_service.repository = repository_mock

    # When, Then
    with pytest.raises(UserNotFoundException):
        await user_service.login(email="email", password="password")


@pytest.mark.asyncio
async def test_login():
    # Given
    user = make_user(
        id=1,
        password=generate_hashed_password(password="password"),
        email="survey@ding.dong",
        username="survey-dingdong",
        is_admin=False,
    )
    repository_mock.get_user_by_email.return_value = user
    user_service.repository = repository_mock
    token = TokenHelper.encode(payload={"user_id": user.id})

    # When
    sut = await user_service.login(email="email", password="password")

    refresh_token_sub_value = await redis_backend.get(key=f"survey-dingdong::{user.id}")
    refresh_token = TokenHelper.encode(
        payload={"sub": refresh_token_sub_value},
        expire_period=60 * 60 * 14,
    )

    # Then
    assert sut.token == token
    assert sut.refresh_token == refresh_token

    await redis_backend.delete(key=f"survey-dingdong::{user.id}")
