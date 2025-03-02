from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import Request

from app.user.container import UserContainer
from app.user.domain.vo import LoginTypeEnum
from core.fastapi.dependencies import IsAdmin, IsAuthenticated, PermissionDependency
from core.fastapi.dependencies.permission import (
    IsParticipant,
    IsResearcher,
    UnauthorizedException,
)

container = UserContainer()


@pytest.fixture
def mock_request() -> Mock:
    return Mock(spec=Request)


@pytest.fixture
def user_service_mock() -> AsyncMock:
    mock = AsyncMock()
    mock.is_admin.return_value = False
    return mock


class TestPermission:
    @pytest.mark.asyncio
    async def test_is_authenticated_unauthorized_when_user_id_is_none(
        self, mock_request: Mock
    ) -> None:
        # Given
        dependency = PermissionDependency(permissions=[IsAuthenticated])
        mock_request.user = AsyncMock(id=None)

        # When, Then
        with pytest.raises(UnauthorizedException):
            await dependency(request=mock_request)

    @pytest.mark.asyncio
    async def test_is_admin_unauthorized_when_not_admin(
        self, mock_request: Mock, user_service_mock: AsyncMock
    ) -> None:
        # Given
        dependency = PermissionDependency(permissions=[IsAdmin])
        mock_request.user = AsyncMock(id=1)

        # When, Then
        with container.user_service.override(user_service_mock):
            with pytest.raises(UnauthorizedException):
                await dependency(request=mock_request)

    @pytest.mark.asyncio
    async def test_is_admin_unauthorized_when_user_id_is_none(
        self, mock_request: Mock, user_service_mock: AsyncMock
    ) -> None:
        # Given
        dependency = PermissionDependency(permissions=[IsAdmin])
        mock_request.user = AsyncMock(id=None)

        # When, Then
        with container.user_service.override(user_service_mock):
            with pytest.raises(UnauthorizedException):
                await dependency(request=mock_request)

    @pytest.mark.asyncio
    async def test_is_researcher_unauthorized_when_login_type_none(
        self, mock_request: Mock
    ) -> None:
        # Given
        dependency = PermissionDependency(permissions=[IsResearcher])
        mock_request.user = AsyncMock(id=1, login_type=None)

        # When, Then
        with pytest.raises(UnauthorizedException):
            await dependency(request=mock_request)

    @pytest.mark.asyncio
    async def test_is_researcher_success_with_researcher_login_type(
        self, mock_request: Mock
    ) -> None:
        # Given
        dependency = PermissionDependency(permissions=[IsResearcher])
        mock_request.user = AsyncMock(id=1, login_type=LoginTypeEnum.Web)

        # When
        result = await dependency(request=mock_request)  # type: ignore [func-returns-value]

        # Then
        assert result is None

    @pytest.mark.asyncio
    async def test_is_participant_unauthorized_when_login_type_none(
        self, mock_request: Mock
    ) -> None:
        # Given
        dependency = PermissionDependency(permissions=[IsParticipant])
        mock_request.user = AsyncMock(id=1, login_type=None)

        # When, Then
        with pytest.raises(UnauthorizedException):
            await dependency(request=mock_request)

    @pytest.mark.asyncio
    async def test_is_participant_success_with_participant_login_type(
        self, mock_request: Mock
    ) -> None:
        # Given
        dependency = PermissionDependency(permissions=[IsParticipant])
        mock_request.user = AsyncMock(id=1, login_type=LoginTypeEnum.App)

        # When
        result = await dependency(request=mock_request)  # type: ignore [func-returns-value]

        # Then
        assert result is None
