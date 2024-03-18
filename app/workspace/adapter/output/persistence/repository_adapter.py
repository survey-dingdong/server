from app.workspace.domain.entity.workspace import Workspace, WorkspaceRead
from app.workspace.domain.repository.workspace import WorkspaceRepo


class WorkspaceRepositoryAdapter:
    def __init__(self, *, workspace_repo: WorkspaceRepo):
        self.workspace_repo = workspace_repo

    async def get_workspaces(self) -> list[WorkspaceRead]:
        workspaces = await self.workspace_repo.get_workspaces()
        return [WorkspaceRead.model_validate(workspace) for workspace in workspaces]

    async def save(self, *, workspace: Workspace) -> None:
        await self.workspace_repo.save(workspace=workspace)
