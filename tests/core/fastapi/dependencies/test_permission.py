from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import Request

from app.user.container import UserContainer
from core.fastapi.dependencies import IsAdmin, IsAuthenticated, PermissionDependency
from core.fastapi.dependencies.permission import UnauthorizedException

container = UserContainer()


@pytest.mark.asyncio
async def test_permission_dependency_is_authenticated():
    # Given
    dependency = PermissionDependency(permissions=[IsAuthenticated])
    request = AsyncMock(spec=Request)
    request.user = Mock(id=None)

    # When, Then
    with pytest.raises(UnauthorizedException):
        await dependency(request=request)


@pytest.mark.asyncio
async def test_permission_dependency_is_admin_user_is_not_admin():
    # Given
    dependency = PermissionDependency(permissions=[IsAdmin])
    request = AsyncMock(spec=Request)
    user_id = 1
    request.user = Mock(id=user_id)
    user_service_mock = AsyncMock()
    user_service_mock.is_admin.return_value = False

    # When, Then
    with container.user_service.override(user_service_mock):
        with pytest.raises(UnauthorizedException):
            await dependency(request=request)


@pytest.mark.asyncio
async def test_permission_dependency_is_admin_user_id_is_none():
    # Given
    dependency = PermissionDependency(permissions=[IsAdmin])
    request = AsyncMock(spec=Request)
    request.user = Mock(id=None)
    user_service_mock = AsyncMock()
    user_service_mock.is_admin.return_value = False

    # When, Then
    with container.user_service.override(user_service_mock):
        with pytest.raises(UnauthorizedException):
            await dependency(request=request)
