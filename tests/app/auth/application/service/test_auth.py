from unittest.mock import AsyncMock

import pytest

from app.auth.adapter.output.external_system.external_system_adapter import (
    ExternalSystemAdapter,
)
from app.auth.application.service.auth import AuthService, DecodeTokenException
from app.user.domain.vo import LoginTypeEnum
from core.helpers.cache import RedisBackend
from tests.support.constants import INVALID_REFRESH_TOKEN, USER_ID_1_TOKEN

port_mock = AsyncMock(spec=ExternalSystemAdapter)
redis_backend = RedisBackend()
auth_service = AuthService(port=port_mock, cache=redis_backend)


@pytest.mark.asyncio
async def test_create_refresh_token_invalid_refresh_token() -> None:
    # Given
    token = INVALID_REFRESH_TOKEN

    # When, Then
    with pytest.raises(DecodeTokenException):
        await auth_service.refresh_access_token(
            access_token=token, refresh_token=token, login_type=LoginTypeEnum.Web
        )


@pytest.mark.asyncio
async def test_create_refresh_token() -> None:
    # Given
    token = USER_ID_1_TOKEN
    await redis_backend.set(response="refresh", key="dingdong-survey::1")

    # When
    sut = await auth_service.refresh_access_token(
        access_token=token, refresh_token=token, login_type=LoginTypeEnum.Web
    )

    # Then
    assert sut.access_token
    assert sut.refresh_token

    await redis_backend.delete(key="dingdong-survey::1")
