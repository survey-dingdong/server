from app.workspace.adapter.output.persistence.repository_adapter import (
    WorkspaceRepositoryAdapter,
)
from app.workspace.application.dto import CreateWorkspaceResponseDTO
from app.workspace.application.exception import (
    TooManyWorkspacesException,
    WorkspaceAccessDeniedException,
    WorkspaceNotFoundeException,
    WrongOrderNoWorkspacesException,
)
from app.workspace.domain.command import CreateWorkspaceCommand
from app.workspace.domain.entity.workspace import Workspace, WorkspaceRead
from app.workspace.domain.usecase.workspace import WorkspaceUseCase
from core.db import Transactional


class WorkspaceService(WorkspaceUseCase):
    def __init__(self, repository: WorkspaceRepositoryAdapter) -> None:
        self.repository = repository

    async def get_workspace_by_id(self, user_id: int, workspace_id: int) -> Workspace:
        workspace = await self.repository.get_workspace_by_id(workspace_id=workspace_id)
        if workspace is None:
            raise WorkspaceNotFoundeException

        if workspace.user_id != user_id:
            raise WorkspaceAccessDeniedException

        return workspace

    async def get_workspace_list(self, user_id: int) -> list[WorkspaceRead]:
        workspaces = await self.repository.get_workspaces(user_id=user_id)

        for idx, workspace in enumerate(workspaces, start=1):
            workspace.order_no = idx

        return [WorkspaceRead.model_validate(workspace) for workspace in workspaces]

    @Transactional()
    async def create_workspace(
        self, command: CreateWorkspaceCommand
    ) -> CreateWorkspaceResponseDTO:
        workspace_count = await self.repository.count(user_id=command.user_id)
        if workspace_count >= 10:
            raise TooManyWorkspacesException

        workspace = Workspace.create(
            user_id=command.user_id,
            title=command.title,
            order_no=workspace_count + 1,
        )
        workspace = await self.repository.save(
            workspace=workspace,
            auto_flush=True,
        )

        return CreateWorkspaceResponseDTO(id=workspace.id)

    @Transactional()
    async def update_workspace(
        self,
        user_id: int,
        workspace_id: int,
        title: str | None,
        order_no: int | None,
    ) -> None:
        workspace = await self.repository.get_workspace_by_id(workspace_id=workspace_id)
        if workspace is None:
            raise WorkspaceNotFoundeException

        if workspace.user_id != user_id:
            raise WorkspaceAccessDeniedException

        if title is not None:
            workspace.change_title(title=title)

        if order_no is not None:
            total_workspace_count = await self.repository.count(user_id=user_id)
            if order_no < 1 or order_no > total_workspace_count:
                raise WrongOrderNoWorkspacesException

            workspaces = await self.repository.get_workspaces(user_id=user_id)
            new_order_no = workspaces[order_no - 1].order_no

            if workspace.order_no < new_order_no:
                new_order_no += 1

            await self.repository.reorder_workspace(
                user_id=user_id, order_no=new_order_no
            )
            workspace.change_order(order_no=new_order_no)

    @Transactional()
    async def delete_workspace(self, user_id: int, workspace_id: int) -> None:
        workspace = await self.repository.get_workspace_by_id(workspace_id=workspace_id)
        if workspace is None:
            raise WorkspaceNotFoundeException

        if workspace.user_id != user_id:
            raise WorkspaceAccessDeniedException

        workspace.is_deleted = True
