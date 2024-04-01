from unittest.mock import AsyncMock

import pytest

from app.workspace.adapter.output.persistence.repository_adapter import (
    WorkspaceRepositoryAdapter,
)
from app.workspace.application.exception import (
    TooManyWorkspacesException,
    WorkspaceNotFoundeException,
)
from app.workspace.application.service.workspace import WorkspaceService
from app.workspace.domain.command import CreateWorkspaceCommand
from app.workspace.domain.entity.workspace import WorkspaceRead
from tests.support.workspace_fixture import make_workspace

repository_mock = AsyncMock(spec=WorkspaceRepositoryAdapter)
workspace_service = WorkspaceService(repository=repository_mock)


@pytest.mark.asyncio
async def test_get_workspace_list():
    # Given
    workspace = WorkspaceRead(id=1, title="workspace", order=1)
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
async def test_update_workspace_not_exist():
    # Given
    repository_mock.get_workspace_by_id.return_value = None
    workspace_service.repository = repository_mock

    # When, Then
    with pytest.raises(WorkspaceNotFoundeException):
        await workspace_service.update_workspace(workspace_id=2, title="title", order=1)


@pytest.mark.asyncio
async def test_update_workspace_title():
    # Given
    workspace = make_workspace(id=1, title="workspace2")
    repository_mock.get_workspace_by_id.return_value = workspace
    workspace_service.repository = repository_mock

    # When
    sut = await workspace_service.update_workspace(
        workspace_id=workspace.id,
        title=workspace.title,
        order=workspace.order,
    )

    # Then
    assert sut.id == 1
    assert sut.title == "workspace2"
    assert sut.order == 1


@pytest.mark.asyncio
async def test_update_workspace_order():
    # Given
    workspace = make_workspace(id=1, order=2)
    repository_mock.get_workspace_by_id.return_value = workspace
    workspace_service.repository = repository_mock

    # When
    sut = await workspace_service.update_workspace(
        workspace_id=workspace.id,
        title=workspace.title,
        order=workspace.order,
    )

    # Then
    assert sut.id == 1
    assert sut.title == "workspace"
    assert sut.order == 2


@pytest.mark.asyncio
async def test_delete_workspace_not_exist():
    # Given
    repository_mock.get_workspace_by_id.return_value = None
    workspace_service.repository = repository_mock

    # When, Then
    with pytest.raises(WorkspaceNotFoundeException):
        await workspace_service.delete_workspace(workspace_id=2)


@pytest.mark.asyncio
async def test_delete_workspace():
    # Given
    workspace = make_workspace(id=1)
    repository_mock.get_workspace_by_id.return_value = workspace
    workspace_service.repository = repository_mock

    # When, Then
    await workspace_service.delete_workspace(workspace_id=workspace.id)
