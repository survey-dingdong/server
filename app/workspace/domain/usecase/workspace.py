from abc import ABC, abstractmethod

from app.workspace.domain.entity.workspace import WorkspaceRead


class WorkspaceUseCase(ABC):
    @abstractmethod
    async def get_workspace_list(self, user_id: int) -> list[WorkspaceRead]:
        """Get workspace list"""
