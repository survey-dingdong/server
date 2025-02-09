from unittest.mock import AsyncMock

import pytest
from pydantic import SecretStr

from app.auth.domain.vo import EmailVerificationType
from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.application.dto import GetUserResponseDTO
from app.user.application.exception import (
    DifferentOAuthProviderException,
    DuplicateEmailOrusernameException,
    OAuthLoginWithPasswordAttemptException,
    PasswordDoesNotMatchException,
    PasswordNotChangedException,
    UnauthorizedAccessException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.user.application.service.user import UserService
from app.user.domain.vo import OauthProviderTypeEnum
from core.helpers.cache import RedisBackend
from core.helpers.token import TokenHelper
from tests.support.user_fixture import make_user, make_user_oauth

repository_mock = AsyncMock(spec=UserRepositoryAdapter)
redis_backend = RedisBackend()
user_service = UserService(repository=repository_mock, cache=redis_backend)


@pytest.mark.asyncio
async def test_get_user_list() -> None:
    # Given
    page = 1
    size = 10
    user = make_user(
        password="password",
        email="survey@ding.dong",
        username="dingdong-survey",
        is_admin=False,
    )
    repository_mock.get_users.return_value = [user]
    repository_mock.get_user_oauth_accounts.return_value = {}
    user_service.repository = repository_mock

    # When
    sut = await user_service.get_user_list(page=page, size=size)

    # Then
    assert len(sut) == 1
    result = sut[0]

    assert result.email == user.email
    assert result.username == user.username
    assert result.is_admin == user.is_admin
    assert result.is_deleted == user.is_deleted
    assert result.oauth_accounts == []

    user_service.repository.get_users.assert_awaited_once_with(page=page, size=size)


@pytest.mark.asyncio
async def test_get_user_me_no_exist() -> None:
    # Given
    repository_mock.get_user_by_id.return_value = None
    user_service.repository = repository_mock

    # When, Then
    with pytest.raises(UserNotFoundException):
        await user_service.get_user_by_id(user_id=1)


@pytest.mark.asyncio
async def test_get_user_me() -> None:
    # Given
    user = GetUserResponseDTO(
        id=1, email="survey@ding.dong", username="dingdong-survey", oauth_accounts=[]
    )
    repository_mock.get_user_by_id.return_value = user
    user_service.repository = repository_mock

    # When
    sut = await user_service.get_user_by_id(user_id=user.id)

    # Then
    assert sut.email == user.email
    assert sut.username == user.username


@pytest.mark.asyncio
async def test_create_user_duplicated() -> None:
    # Given
    # When, Then
    with pytest.raises(UnauthorizedAccessException):
        await user_service.create_user(
            email="survey@ding.dong",
            password=SecretStr("Qwer1234!"),
            username="dingdong-survey",
        )


@pytest.mark.asyncio
async def test_create_user_unauthorized() -> None:
    # Given
    user = make_user(
        password="password",
        email="survey@ding.dong",
        username="dingdong-survey",
        is_admin=False,
    )
    signup_redis_key = f"dingdong-survey::{EmailVerificationType.SIGNUP}::{user.email}"
    await user_service.cache.set(response="signup_code", key=signup_redis_key)

    repository_mock.get_user_by_email.return_value = user
    user_service.repository = repository_mock

    # When, Then
    with pytest.raises(DuplicateEmailOrusernameException):
        await user_service.create_user(
            email=user.email,
            password=SecretStr("password"),
            username=user.username,
        )

    await user_service.cache.delete(key=signup_redis_key)


@pytest.mark.asyncio
async def test_create_user() -> None:
    # Given
    repository_mock.get_user_by_email.return_value = None
    user_service.repository = repository_mock

    user = make_user(
        id=1,
        password="password",
        email="survey@ding.dong",
        username="dingdong-survey",
        is_admin=False,
    )

    signup_redis_key = f"dingdong-survey::{EmailVerificationType.SIGNUP}::{user.email}"
    await user_service.cache.set(response="signup_code", key=signup_redis_key)

    # When
    sut = await user_service.create_user(
        email=user.email,
        password=SecretStr("password"),
        username=user.username,
    )

    # Then
    assert "token" in sut.model_dump_json()


@pytest.mark.asyncio
async def test_is_admin_user_no_exist() -> None:
    # Given
    repository_mock.get_user_by_id.return_value = None
    user_service.repository = repository_mock

    # When
    sut = await user_service.is_admin(user_id=1)

    # Then
    assert sut is False


@pytest.mark.asyncio
async def test_is_admin_user_is_not_admin() -> None:
    # Given
    user = make_user(
        password="password",
        email="survey@ding.dong",
        username="dingdong-survey",
        is_admin=False,
    )
    repository_mock.get_user_by_id.return_value = user
    user_service.repository = repository_mock

    # When
    sut = await user_service.is_admin(user_id=user.id)

    # Then
    assert sut is False


@pytest.mark.asyncio
async def test_is_admin() -> None:
    # Given
    user = make_user(
        password="password",
        email="survey@ding.dong",
        username="dingdong-survey",
        is_admin=True,
    )
    repository_mock.get_user_by_id.return_value = user
    user_service.repository = repository_mock

    # When
    sut = await user_service.is_admin(user_id=user.id)

    # Then
    assert sut is True


@pytest.mark.asyncio
async def test_login_user_no_exist() -> None:
    # Given
    repository_mock.get_user_by_email.return_value = None
    user_service.repository = repository_mock

    # When, Then
    with pytest.raises(UserNotFoundException):
        await user_service.login(email="email", password=SecretStr("password"))


@pytest.mark.asyncio
async def test_oauth_login_with_password() -> None:
    # Given
    user = make_user(
        id=1,
        password=None,
        email="survey@ding.dong",
        username="dingdong-survey",
        is_admin=False,
    )
    repository_mock.get_user_by_email.return_value = user
    user_service.repository = repository_mock

    # When, Then
    with pytest.raises(OAuthLoginWithPasswordAttemptException):
        await user_service.login(
            email="survey@ding.dong", password=SecretStr("password")
        )


@pytest.mark.asyncio
async def test_login_not_matched_password() -> None:
    # Given
    user = make_user(
        id=1,
        password="password",
        email="survey@ding.dong",
        username="dingdong-survey",
        is_admin=False,
    )
    repository_mock.get_user_by_email.return_value = user
    user_service.repository = repository_mock

    # When, Then
    with pytest.raises(PasswordDoesNotMatchException):
        await user_service.login(
            email="survey@ding.dong", password=SecretStr("wrong password")
        )


@pytest.mark.asyncio
async def test_login() -> None:
    # Given
    user = make_user(
        id=1,
        password="password",
        email="survey@ding.dong",
        username="dingdong-survey",
        is_admin=False,
    )
    repository_mock.get_user_by_email.return_value = user
    user_service.repository = repository_mock
    token = TokenHelper.encode(payload={"user_id": user.id})

    # When
    sut = await user_service.login(
        email="survey@ding.dong", password=SecretStr("password")
    )

    # Then
    assert sut.token == token


@pytest.mark.asyncio
async def test_oauth_login_already_exist() -> None:
    # Given
    user = make_user(
        id=1,
        password="password",
        email="survey@ding.dong",
        username="dingdong-survey",
        is_admin=False,
    )
    # Given
    repository_mock.get_user_by_email.return_value = user
    user_service.repository = repository_mock

    # When, Then
    with pytest.raises(UserAlreadyExistsException):
        await user_service.oauth_login(
            email=user.email,
            username=user.username,
            oauth_id="oauth_id",
            provider=OauthProviderTypeEnum.GOOGLE,
        )


@pytest.mark.asyncio
async def test_oauth_login_diff_provider() -> None:
    # Given
    user = make_user(
        id=1,
        password=None,
        email="survey@ding.dong",
        username="dingdong-survey",
        is_admin=False,
    )
    user_oauth = make_user_oauth(
        user_id=user.id,
        oauth_id="oauth_id",
        provider=OauthProviderTypeEnum.GOOGLE,
    )
    # Given
    repository_mock.get_user_by_email.return_value = user
    repository_mock.get_user_by_oauth_id.return_value = user_oauth
    user_service.repository = repository_mock

    # When, Then
    with pytest.raises(DifferentOAuthProviderException):
        await user_service.oauth_login(
            email=user.email,
            username=user.username,
            oauth_id=user_oauth.oauth_id,
            provider=OauthProviderTypeEnum.FACEBOOK,
        )


@pytest.mark.asyncio
async def test_oauth_login_first() -> None:
    # Given
    user = make_user(
        id=1,
        password=None,
        email="survey@ding.dong",
        username="dingdong-survey",
        is_admin=False,
    )
    user_oauth = make_user_oauth(
        user_id=user.id,
        oauth_id="oauth_id",
        provider=OauthProviderTypeEnum.GOOGLE,
    )
    # Given
    repository_mock.get_user_by_email.return_value = None
    repository_mock.add.return_value = user
    repository_mock.get_user_by_oauth_id.return_value = None
    token = TokenHelper.encode(payload={"user_id": user.id})

    # When
    sut = await user_service.oauth_login(
        email=user.email,
        username=user.username,
        provider=user_oauth.provider,
        oauth_id=user_oauth.oauth_id,
    )

    # Then
    assert sut.token == token


@pytest.mark.asyncio
async def test_oauth_login() -> None:
    # Given
    user = make_user(
        id=1,
        password=None,
        email="survey@ding.dong",
        username="dingdong-survey",
        is_admin=False,
    )
    user_oauth = make_user_oauth(
        user_id=user.id,
        oauth_id="oauth_id",
        provider=OauthProviderTypeEnum.GOOGLE,
    )
    # Given
    repository_mock.get_user_by_email.return_value = user
    token = TokenHelper.encode(payload={"user_id": user.id})

    # When
    sut = await user_service.oauth_login(
        email=user.email,
        username=user.username,
        oauth_id=user_oauth.oauth_id,
        provider=user_oauth.provider,
    )

    # Then
    assert sut.token == token


@pytest.mark.asyncio
async def test_change_password_not_matched() -> None:
    # Given
    user = make_user(
        id=1,
        password="password",
        email="survey@ding.dong",
        username="dingdong-survey",
        is_admin=False,
    )
    repository_mock.get_user_by_id.return_value = user
    user_service.repository = repository_mock

    # When, Then
    with pytest.raises(PasswordDoesNotMatchException):
        await user_service.change_password(
            user_id=user.id,
            old_password=SecretStr("wrong password"),
            new_password=SecretStr("new password"),
        )


@pytest.mark.asyncio
async def test_change_password_not_changed() -> None:
    # Given
    user = make_user(
        id=1,
        password="password",
        email="survey@ding.dong",
        username="dingdong-survey",
        is_admin=False,
    )
    repository_mock.get_user_by_id.return_value = user
    user_service.repository = repository_mock

    # When, Then
    with pytest.raises(PasswordNotChangedException):
        await user_service.change_password(
            user_id=user.id,
            old_password=SecretStr("password"),
            new_password=SecretStr("password"),
        )


@pytest.mark.asyncio
async def test_change_password() -> None:
    # Given
    user = make_user(
        id=1,
        password="password",
        email="survey@ding.dong",
        username="dingdong-survey",
        is_admin=False,
    )
    repository_mock.get_user_by_id.return_value = user
    user_service.repository = repository_mock

    # When, Then
    await user_service.change_password(
        user_id=user.id,
        old_password=SecretStr("password"),
        new_password=SecretStr("new password"),
    )


@pytest.mark.asyncio
async def test_reset_password_unauthorized() -> None:
    # Given
    user = make_user(
        id=1,
        password="password",
        email="survey@ding.dong",
        username="dingdong-survey",
        is_admin=False,
    )
    repository_mock.get_user_by_email.return_value = user
    user_service.repository = repository_mock

    # When, Then
    with pytest.raises(UnauthorizedAccessException):
        await user_service.reset_password(
            email=user.email,
            new_password=SecretStr("new password"),
        )


@pytest.mark.asyncio
async def test_reset_password() -> None:
    # Given
    user = make_user(
        id=1,
        password="password",
        email="survey@ding.dong",
        username="dingdong-survey",
        is_admin=False,
    )

    # email verification code is cached
    reset_pw_redis_key = (
        f"dingdong-survey::{EmailVerificationType.RESET_PASSWORD}::{user.email}"
    )
    await user_service.cache.set(response="cached_code", key=reset_pw_redis_key)

    repository_mock.get_user_by_email.return_value = user
    user_service.repository = repository_mock

    # When, Then
    await user_service.reset_password(
        email=user.email,
        new_password=SecretStr("new password"),
    )

    await user_service.cache.delete(key=reset_pw_redis_key)
