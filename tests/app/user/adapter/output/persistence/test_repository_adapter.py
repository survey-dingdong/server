from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.domain.repository.user import UserRepo
from tests.support.user_fixture import make_user

user_repo_mock = AsyncMock(spec=UserRepo)
repository_adapter = UserRepositoryAdapter(repository=user_repo_mock)


@pytest.mark.asyncio
async def test_get_users(session: AsyncSession):
    # Given
    page = 1
    size = 1
    user = make_user(
        id=1,
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )
    user_repo_mock.get_users.return_value = [user]
    repository_adapter.repository = user_repo_mock

    # When
    sut = await repository_adapter.get_users(page=page, size=size)

    # Then
    assert len(sut) == 1
    result = sut[0]
    assert result.email == user.email
    assert result.username == user.username
    repository_adapter.repository.get_users.assert_awaited_once_with(
        page=page, size=size
    )


@pytest.mark.asyncio
async def test_get_user_by_id(session: AsyncSession):
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )
    user_repo_mock.get_user_by_id.return_value = user
    repository_adapter.repository = user_repo_mock

    # When
    sut = await repository_adapter.get_user_by_id(user_id=user.id)

    # Then
    assert sut is not None
    assert sut.id == user.id
    assert sut.password == user.password
    assert sut.email == user.email
    assert sut.username == user.username
    assert sut.is_admin == user.is_admin
    repository_adapter.repository.get_user_by_id.assert_awaited_once_with(
        user_id=user.id
    )


@pytest.mark.asyncio
async def test_get_user_by_email(session: AsyncSession):
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )
    user_repo_mock.get_user_by_email.return_value = user
    repository_adapter.repository = user_repo_mock

    # When
    sut = await repository_adapter.get_user_by_email(email=user.email)

    # Then
    assert sut is not None
    assert sut.id == user.id
    assert sut.password == user.password
    assert sut.email == user.email
    assert sut.username == user.username
    assert sut.is_admin == user.is_admin
    repository_adapter.repository.get_user_by_email.assert_awaited_once_with(
        email=user.email
    )


@pytest.mark.asyncio
async def test_save(session: AsyncSession):
    # Given
    user = make_user(
        id=1,
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )
    user_repo_mock.save.return_value = user
    repository_adapter.repository = user_repo_mock

    # When
    sut = await repository_adapter.save(user=user, auto_flush=True)

    # Then
    assert sut.id == user.id
    assert sut.email == user.email
    assert sut.username == user.username
