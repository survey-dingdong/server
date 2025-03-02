from unittest.mock import AsyncMock

import pytest

from app.auth.adapter.output.external_system.external_system_adapter import (
    ExternalSystemAdapter,
)
from app.auth.application.service.auth import AuthService, DecodeTokenException
from app.user.domain.vo import LoginTypeEnum
from core.helpers.token import TokenHelper
from tests.support.constants import DEFAULT_USER_ID


@pytest.fixture
def port_mock() -> AsyncMock:
    return AsyncMock(spec=ExternalSystemAdapter)


@pytest.fixture
def redis_backend() -> AsyncMock:
    mock = AsyncMock()
    mock.get_refresh_token.return_value = "refresh_token_value"
    return mock


@pytest.fixture
def auth_service(port_mock: AsyncMock, redis_backend: AsyncMock) -> AuthService:
    return AuthService(port=port_mock, cache=redis_backend)


class TestAuthService:
    @pytest.mark.asyncio
    async def test_with_invalid_refresh_token(
        self, auth_service: AuthService, access_token: str, invalid_refresh_token: str
    ) -> None:
        # When & Then
        with pytest.raises(DecodeTokenException):
            await auth_service.refresh_access_token(
                access_token=access_token,
                refresh_token=invalid_refresh_token,
                login_type=LoginTypeEnum.Web,
            )

    @pytest.mark.asyncio
    async def test_with_valid_tokens(
        self, auth_service: AuthService, access_token: str, refresh_token: str
    ) -> None:
        # When
        result = await auth_service.refresh_access_token(
            access_token=access_token,
            refresh_token=refresh_token,
            login_type=LoginTypeEnum.Web,
        )

        # Then
        decoded_access_token = TokenHelper.decode(result.access_token)
        decoded_refresh_token = TokenHelper.decode(result.refresh_token)

        assert decoded_access_token["user_id"] == DEFAULT_USER_ID
        assert decoded_access_token["login_type"] == LoginTypeEnum.Web
        assert decoded_refresh_token["sub"] == "refresh_token_value"
