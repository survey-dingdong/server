from abc import ABC, abstractmethod

from app.workspace.domain.entity.workspace import Workspace


class WorkspaceRepo(ABC):
    @abstractmethod
    async def get_workspaces(self, user_id: int) -> list[Workspace]:
        """Get workspace list"""

    @abstractmethod
    async def get_workspace_by_id(self, workspace_id: int) -> Workspace | None:
        """Get workspace by id"""

    @abstractmethod
    async def reorder_workspace(self, user_id: int, order_no: int) -> None:
        """Reorder workspace"""

    @abstractmethod
    async def count(self, user_id: int) -> int:
        """Count workspaces"""

    @abstractmethod
    async def save(self, workspace: Workspace, auto_flush: bool) -> Workspace:
        """Save workspace"""
