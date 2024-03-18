from abc import ABC, abstractmethod

from app.workspace.domain.entity.workspace import Workspace


class WorkspaceRepo(ABC):
    @abstractmethod
    async def get_workspaces(self) -> list[Workspace]:
        """Get workspace list"""

    @abstractmethod
    async def save(self, *, workspace: Workspace) -> None:
        """Save workspace"""
