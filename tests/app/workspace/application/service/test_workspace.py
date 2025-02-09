from unittest.mock import AsyncMock

import pytest

from app.workspace.adapter.output.persistence.repository_adapter import (
    WorkspaceRepositoryAdapter,
)
from app.workspace.application.dto import GetWorkspaceRepsonseDTO
from app.workspace.application.exception import (
    TooManyWorkspacesException,
    WorkspaceAccessDeniedException,
    WorkspaceNotFoundeException,
)
from app.workspace.application.service.workspace import WorkspaceService
from tests.support.workspace_fixture import make_workspace

repository_mock = AsyncMock(spec=WorkspaceRepositoryAdapter)
workspace_service = WorkspaceService(repository=repository_mock)


@pytest.mark.asyncio
async def test_get_workspace_list() -> None:
    # Given
    workspace = GetWorkspaceRepsonseDTO(id=1, title="workspace", order_no=1)
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
async def test_create_workspace_too_many() -> None:
    # Given
    repository_mock.count.return_value = 10
    workspace_service.repository = repository_mock

    # When, Then
    with pytest.raises(TooManyWorkspacesException):
        await workspace_service.create_workspace(user_id=1, title="workspace")


@pytest.mark.asyncio
async def test_create_workspace() -> None:
    # Given
    repository_mock.count.return_value = 0
    workspace_service.repository = repository_mock

    # When
    sut = await workspace_service.create_workspace(user_id=1, title="workspace")

    # Then
    assert sut.id == 1


@pytest.mark.asyncio
async def test_update_workspace_not_exist() -> None:
    # Given
    repository_mock.get_workspace_by_id.return_value = None
    workspace_service.repository = repository_mock

    # When, Then
    with pytest.raises(WorkspaceNotFoundeException):
        await workspace_service.update_workspace(
            user_id=1, workspace_id=2, title="title", order_no=1
        )


@pytest.mark.asyncio
async def test_update_workspace_access_denied() -> None:
    # Given
    workspace = make_workspace(id=1)
    repository_mock.get_workspace_by_id.return_value = workspace
    workspace_service.repository = repository_mock

    # When, Then
    with pytest.raises(WorkspaceAccessDeniedException):
        await workspace_service.update_workspace(
            user_id=2, workspace_id=1, title="title", order_no=None
        )


@pytest.mark.asyncio
async def test_update_workspace_title() -> None:
    # Given
    workspace = make_workspace(id=1, title="workspace2")
    repository_mock.get_workspace_by_id.return_value = workspace
    workspace_service.repository = repository_mock

    # When
    await workspace_service.update_workspace(
        user_id=1,
        workspace_id=workspace.id,
        title=workspace.title,
        order_no=None,
    )


@pytest.mark.asyncio
async def test_update_workspace_order() -> None:
    # Given
    workspace1 = make_workspace(id=1, order_no=1)
    workspace2 = make_workspace(id=2, order_no=2)
    repository_mock.get_workspace_by_id.return_value = workspace2
    workspace_service.repository = repository_mock

    repository_mock.count.return_value = 2

    repository_mock.get_workspaces.return_value = [workspace1, workspace2]

    # When
    await workspace_service.update_workspace(
        user_id=1,
        workspace_id=workspace2.id,
        title=workspace2.title,
        order_no=workspace1.order_no,
    )


@pytest.mark.asyncio
async def test_delete_workspace_not_exist() -> None:
    # Given
    repository_mock.get_workspace_by_id.return_value = None
    workspace_service.repository = repository_mock

    # When, Then
    with pytest.raises(WorkspaceNotFoundeException):
        await workspace_service.delete_workspace(user_id=1, workspace_id=2)


@pytest.mark.asyncio
async def test_delete_workspace_access_denied() -> None:
    # Given
    workspace = make_workspace(id=1)
    repository_mock.get_workspace_by_id.return_value = workspace
    workspace_service.repository = repository_mock

    # When, Then
    with pytest.raises(WorkspaceAccessDeniedException):
        await workspace_service.delete_workspace(user_id=2, workspace_id=2)


@pytest.mark.asyncio
async def test_delete_workspace() -> None:
    # Given
    workspace = make_workspace(id=1)
    repository_mock.get_workspace_by_id.return_value = workspace
    workspace_service.repository = repository_mock

    # When, Then
    await workspace_service.delete_workspace(user_id=1, workspace_id=workspace.id)
