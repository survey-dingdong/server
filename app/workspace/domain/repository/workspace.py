from abc import ABC, abstractmethod

from app.workspace.domain.entity.workspace import Workspace


class WorkspaceRepo(ABC):
    @abstractmethod
    async def get_workspaces(self, user_id: int) -> list[Workspace]:
        """Get workspace list"""

    @abstractmethod
    async def count(self, user_id: int) -> int:
        """Count workspaces"""

    @abstractmethod
    async def save(self, workspace: Workspace, auto_flush: bool) -> Workspace:
        """Save workspace"""
