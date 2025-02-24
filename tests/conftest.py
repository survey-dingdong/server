import asyncio
from asyncio import AbstractEventLoop
from collections.abc import AsyncGenerator, Generator, Iterator
from unittest.mock import Mock
from uuid import uuid4

import jwt
import pytest
import pytest_asyncio
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from app.user.domain.vo import LoginTypeEnum
from core.config import config
from core.db.session import reset_session_context
from core.db.session import session as db_session
from core.db.session import set_session_context
from tests.support.constants import DEFAULT_USER_ID
from tests.support.test_db_coordinator import TestDbCoordinator

test_db_coordinator = TestDbCoordinator()


@pytest.fixture(scope="function", autouse=True)
def session_context() -> Generator[None, None, None]:
    session_id = str(uuid4())
    context = set_session_context(session_id=session_id)
    yield
    reset_session_context(context=context)


@pytest.fixture(scope="session")
def event_loop() -> Iterator[AbstractEventLoop]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def session() -> AsyncGenerator[
    async_scoped_session[AsyncSession],
    None,
]:
    test_db_coordinator.apply_alembic()
    yield db_session
    await db_session.remove()
    test_db_coordinator.truncate_all()


@pytest.fixture(scope="function")
def invalid_access_token() -> str:
    token = jwt.encode(
        payload={
            "user_id": DEFAULT_USER_ID,
            "login_type": LoginTypeEnum.Web,
        },
        key=config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM,
    )
    return token


@pytest.fixture(scope="function")
def access_token() -> str:
    token = jwt.encode(
        payload={
            "user_id": DEFAULT_USER_ID,
            "login_type": LoginTypeEnum.Web,
        },
        key=config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM,
    )
    return token


@pytest.fixture(scope="function")
def invalid_refresh_token() -> str:
    token = jwt.encode(
        payload={
            "sub": "invalid_refresh_token_value",
        },
        key=config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM,
    )
    return token


@pytest.fixture(scope="function")
def refresh_token() -> str:
    token = jwt.encode(
        payload={
            "sub": "refresh_token_value",
        },
        key=config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM,
    )
    return token
