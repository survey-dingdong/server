from abc import ABC, abstractmethod

from app.workspace.domain.entity.workspace import Workspace


class WorkspaceUseCase(ABC):
    @abstractmethod
    async def get_workspace_list(self) -> list[Workspace]:
        """Get workspace list"""
