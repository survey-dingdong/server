from app.workspace.domain.entity.workspace import Workspace
from app.workspace.domain.repository.workspace import WorkspaceRepo


class WorkspaceRepositoryAdapter:
    def __init__(self, repository: WorkspaceRepo):
        self.repository = repository

    async def get_workspaces(self, user_id: int) -> list[Workspace]:
        return await self.repository.get_workspaces(user_id=user_id)

    async def get_workspace_by_id(self, workspace_id: int) -> Workspace | None:
        return await self.repository.get_workspace_by_id(workspace_id=workspace_id)

    async def reorder_workspace(self, user_id: int, order_no: int) -> None:
        await self.repository.reorder_workspace(user_id=user_id, order_no=order_no)

    async def count(self, user_id: int) -> int:
        return await self.repository.count(user_id=user_id)

    async def save(self, workspace: Workspace, auto_flush: bool = False) -> Workspace:
        return await self.repository.save(workspace=workspace, auto_flush=auto_flush)
