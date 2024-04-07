from abc import ABC, abstractmethod

from app.workspace.application.dto import (
    CreateWorkspaceResponseDTO,
    GetWorkspaceRepsonseDTO,
)
from app.workspace.domain.command import CreateWorkspaceCommand
from app.workspace.domain.entity.workspace import WorkspaceRead


class WorkspaceUseCase(ABC):
    @abstractmethod
    async def get_workspace_list(
        self, user_id: int, page: int, size: int
    ) -> list[WorkspaceRead]:
        """Get workspace list"""

    @abstractmethod
    async def create_workspace(
        self, command: CreateWorkspaceCommand
    ) -> CreateWorkspaceResponseDTO:
        """Create workspace"""

    @abstractmethod
    async def update_workspace(
        self, workspace_id: int, title: str | None, order: int | None
    ) -> GetWorkspaceRepsonseDTO:
        """Update workspace"""

    @abstractmethod
    async def delete_workspace(self, workspace_id: int) -> None:
        """Delete workspace"""
