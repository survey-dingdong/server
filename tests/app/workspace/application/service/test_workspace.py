from unittest.mock import AsyncMock

import pytest

from app.workspace.adapter.output.persistence.repository_adapter import (
    WorkspaceRepositoryAdapter,
)
from app.workspace.application.exception import TooManyWorkspacesException
from app.workspace.application.service.workspace import WorkspaceService
from app.workspace.domain.command import CreateWorkspaceCommand
from app.workspace.domain.entity.workspace import WorkspaceRead

repository_mock = AsyncMock(spec=WorkspaceRepositoryAdapter)
workspace_service = WorkspaceService(repository=repository_mock)


@pytest.mark.asyncio
async def test_get_workspace_list():
    # Given
    workspace = WorkspaceRead(id=1, title="workspace")
    repository_mock.get_workspaces.return_value = [workspace]
    workspace_service.repository = repository_mock

    # When
    sut = await workspace_service.get_workspace_list(user_id=1)

    # Then
    assert len(sut) == 1
    result = sut[0]
    assert result.id == workspace.id
    assert result.title == workspace.title
    workspace_service.repository.get_workspaces.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_workspace_too_many():
    # Given
    command = CreateWorkspaceCommand(user_id=1, title="workspace")

    repository_mock.count.return_value = 10
    workspace_service.repository = repository_mock

    # When, Then
    with pytest.raises(TooManyWorkspacesException):
        await workspace_service.create_workspace(command=command)


@pytest.mark.asyncio
async def test_create_workspace():
    # Given
    command = CreateWorkspaceCommand(user_id=1, title="workspace")
    repository_mock.count.return_value = 0
    workspace_service.repository = repository_mock

    # When
    sut = await workspace_service.create_workspace(command=command)

    # Then
    assert sut.id == 1


@pytest.mark.asyncio
async def test_update_workspace():
    pass
