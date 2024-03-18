from app.workspace.adapter.output.persistence.repository_adapter import (
    WorkspaceRepositoryAdapter,
)
from app.workspace.domain.entity.workspace import WorkspaceRead
from app.workspace.domain.usecase.workspace import WorkspaceUseCase


class WorkspaceService(WorkspaceUseCase):
    def __init__(self, repository: WorkspaceRepositoryAdapter) -> None:
        self.repository = repository

    async def get_workspace_list(self) -> list[WorkspaceRead]:
        return await self.repository.get_workspaces()
