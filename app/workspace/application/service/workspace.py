from app.workspace.adapter.output.persistence.repository_adapter import (
    WorkspaceRepositoryAdapter,
)
from app.workspace.application.dto import CreateWorkspaceResponseDTO
from app.workspace.application.exception import TooManyWorkspacesException
from app.workspace.domain.command import CreateWorkspaceCommand
from app.workspace.domain.entity.workspace import Workspace, WorkspaceRead
from app.workspace.domain.usecase.workspace import WorkspaceUseCase
from core.db import Transactional


class WorkspaceService(WorkspaceUseCase):
    def __init__(self, repository: WorkspaceRepositoryAdapter) -> None:
        self.repository = repository

    async def get_workspace_list(self, user_id: int) -> list[WorkspaceRead]:
        return await self.repository.get_workspaces(user_id=user_id)

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
