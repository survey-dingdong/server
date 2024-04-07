from app.workspace.adapter.output.persistence.repository_adapter import (
    WorkspaceRepositoryAdapter,
)
from app.workspace.application.dto import (
    CreateWorkspaceResponseDTO,
    GetWorkspaceRepsonseDTO,
)
from app.workspace.application.exception import (
    TooManyWorkspacesException,
    WorkspaceNotFoundeException,
)
from app.workspace.domain.command import CreateWorkspaceCommand
from app.workspace.domain.entity.workspace import Workspace, WorkspaceRead
from app.workspace.domain.usecase.workspace import WorkspaceUseCase
from core.db import Transactional


class WorkspaceService(WorkspaceUseCase):
    def __init__(self, repository: WorkspaceRepositoryAdapter) -> None:
        self.repository = repository

    async def get_workspace_list(
        self, user_id: int, page: int, size: int
    ) -> list[WorkspaceRead]:
        return await self.repository.get_workspaces(
            user_id=user_id, page=page, size=size
        )

    @Transactional()
    async def create_workspace(
        self, command: CreateWorkspaceCommand
    ) -> CreateWorkspaceResponseDTO:
        workspace_count = await self.repository.count(user_id=command.user_id)
        if workspace_count >= 10:
            raise TooManyWorkspacesException

        workspace = Workspace.create(
            user_id=command.user_id,
            title=command.title,
        )
        workspace = await self.repository.save(
            workspace=workspace,
            auto_flush=True,
        )

        return CreateWorkspaceResponseDTO(id=workspace.id)

    @Transactional()
    async def update_workspace(
        self, workspace_id: int, title: str | None, order: int | None
    ) -> GetWorkspaceRepsonseDTO:
        workspace = await self.repository.get_workspace_by_id(workspace_id=workspace_id)
        if workspace is None:
            raise WorkspaceNotFoundeException

        if title:
            workspace.change_title(title=title)

        if order:
            workspace.change_order(order=order)
            await self.repository.reorder_workspace(changed_order=order)

        return GetWorkspaceRepsonseDTO(
            id=workspace.id, title=workspace.title, order=workspace.order
        )

    @Transactional()
    async def delete_workspace(self, workspace_id: int) -> None:
        workspace = await self.repository.get_workspace_by_id(workspace_id=workspace_id)
        if workspace is None:
            raise WorkspaceNotFoundeException

        await self.repository.delete(workspace_id=workspace_id)
