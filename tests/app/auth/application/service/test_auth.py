from unittest.mock import AsyncMock

import pytest

from app.auth.adapter.output.external_system.external_system_adapter import (
    ExternalSystemAdapter,
)
from app.auth.application.service.auth import AuthService, DecodeTokenException
from core.helpers.cache import RedisBackend
from tests.support.constants import INVALID_REFRESH_TOKEN, USER_ID_1_TOKEN

port_mock = AsyncMock(spec=ExternalSystemAdapter)
redis_backend = RedisBackend()
auth_service = AuthService(port=port_mock, cache=redis_backend)


@pytest.mark.asyncio
async def test_create_refresh_token_invalid_refresh_token():
    # Given
    token = INVALID_REFRESH_TOKEN

    # When, Then
    with pytest.raises(DecodeTokenException):
        await auth_service.create_refresh_token(token=token, refresh_token=token)


@pytest.mark.asyncio
async def test_create_refresh_token():
    # Given
    token = USER_ID_1_TOKEN
    await redis_backend.set(response="refresh", key="survey-dingdong::1")

    # When
    sut = await auth_service.create_refresh_token(token=token, refresh_token=token)

    # Then
    assert sut.token
    assert sut.refresh_token

    await redis_backend.delete(key="survey-dingdong::1")
