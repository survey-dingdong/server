from app.workspace.domain.entity.workspace import Workspace, WorkspaceRead
from app.workspace.domain.repository.workspace import WorkspaceRepo


class WorkspaceRepositoryAdapter:
    def __init__(self, workspace_repo: WorkspaceRepo):
        self.workspace_repo = workspace_repo

    async def get_workspaces(self, user_id: int) -> list[WorkspaceRead]:
        workspaces: list[Workspace] = await self.workspace_repo.get_workspaces(
            user_id=user_id
        )
        return [WorkspaceRead.model_validate(workspace) for workspace in workspaces]

    async def get_workspace_by_id(self, workspace_id: int) -> Workspace | None:
        return await self.workspace_repo.get_workspace_by_id(workspace_id=workspace_id)

    async def reorder_workspace(self, changed_order: int) -> None:
        await self.workspace_repo.reorder_workspace(changed_order=changed_order)

    async def count(self, user_id: int) -> int:
        return await self.workspace_repo.count(user_id=user_id)

    async def delete(self, workspace_id: int) -> None:
        await self.workspace_repo.delete(workspace_id=workspace_id)

    async def save(self, workspace: Workspace, auto_flush: bool = False) -> Workspace:
        return await self.workspace_repo.save(
            workspace=workspace, auto_flush=auto_flush
        )
