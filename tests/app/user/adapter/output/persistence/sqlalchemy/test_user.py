import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.user.domain.entity.user import User
from tests.support.user_fixture import make_user

user_repo = UserSQLAlchemyRepo()


@pytest.mark.asyncio
async def test_get_users(session: AsyncSession):
    # Given
    user_1 = make_user(
        password="password",
        email="a@b.c",
        username="survey-dingdong",
        is_admin=True,
    )
    user_2 = make_user(
        password="password2",
        email="b@b.c",
        username="test",
        is_admin=False,
    )
    session.add_all([user_1, user_2])
    await session.commit()

    # When
    sut = await user_repo.get_users(page=1, size=12)

    # Then
    assert len(sut) == 2
    saved_user_1 = sut[0]
    assert saved_user_1.password == user_1.password
    assert saved_user_1.email == user_1.email
    assert saved_user_1.username == user_1.username
    assert saved_user_1.is_admin == user_1.is_admin

    saved_user_2 = sut[1]
    assert saved_user_2.password == user_2.password
    assert saved_user_2.email == user_2.email
    assert saved_user_2.username == user_2.username
    assert saved_user_2.is_admin == user_2.is_admin


@pytest.mark.asyncio
async def test_get_user_by_email_or_username(session: AsyncSession):
    # Given
    email = "a@b.c"
    username = "survey-dingdong"
    user = make_user(
        password="password2",
        email=email,
        username=username,
        is_admin=False,
    )
    session.add(user)
    await session.commit()

    # When
    sut = await user_repo.get_user_by_email_or_username(email=email, username=username)

    # Then
    assert isinstance(sut, User)
    assert sut.id == user.id
    assert sut.email == email
    assert sut.username == username


@pytest.mark.asyncio
async def test_get_user_by_id(session: AsyncSession):
    # Given
    user_id = 1

    # When
    sut = await user_repo.get_user_by_id(user_id=user_id)

    # Then
    assert sut is None


@pytest.mark.asyncio
async def test_get_user_by_email(session: AsyncSession):
    # Given
    email = "b@c.d"
    password = "survey-dingdong"
    user = make_user(
        password=password,
        email=email,
        username="survey-dingdong",
        is_admin=False,
    )
    session.add(user)
    await session.commit()

    # When
    sut = await user_repo.get_user_by_email(email=email)

    # Then
    assert isinstance(sut, User)
    assert sut.id == user.id
    assert sut.email == email
    assert sut.password == password


@pytest.mark.asyncio
async def test_save(session: AsyncSession):
    # Given
    email = "b@c.d"
    password = "survey-dingdong"
    user = make_user(
        password=password,
        email=email,
        username="survey-dingdong",
        is_admin=False,
    )

    # When, Then
    await user_repo.save(user=user)
