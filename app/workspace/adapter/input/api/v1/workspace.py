from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from app.workspace.adapter.input.api.v1.request import (
    CreateWorkspaceRequest,
    UpdateWorkspaceRequest,
)
from app.workspace.adapter.input.api.v1.response import (
    CreateWorkspaceResponse,
    GetWorkspaceListResponse,
)
from app.workspace.container import WorkspaceContainer
from app.workspace.domain.command import CreateWorkspaceCommand
from app.workspace.domain.usecase.workspace import WorkspaceUseCase
from core.fastapi.dependencies import IsAuthenticated, PermissionDependency

workspace_router = APIRouter()


@workspace_router.get(
    "",
    response_model=list[GetWorkspaceListResponse],
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def get_workspace_list(
    auth_info: Request,
    usecase: WorkspaceUseCase = Depends(Provide[WorkspaceContainer.workspace_service]),
):
    return await usecase.get_workspace_list(user_id=auth_info.user.id)


@workspace_router.post(
    "",
    response_model=CreateWorkspaceResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def create_workspace(
    auth_info: Request,
    request: CreateWorkspaceRequest,
    usecase: WorkspaceUseCase = Depends(Provide[WorkspaceContainer.workspace_service]),
):
    command = CreateWorkspaceCommand(user_id=auth_info.user.id, title=request.title)
    return await usecase.create_workspace(command=command)


@workspace_router.patch(
    "/{workspace_id}",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def update_workspace(
    auth_info: Request,
    workspace_id: int,
    request: UpdateWorkspaceRequest,
    usecase: WorkspaceUseCase = Depends(Provide[WorkspaceContainer.workspace_service]),
):
    return await usecase.update_workspace(
        user_id=auth_info.user.id,
        workspace_id=workspace_id,
        title=request.title,
        order_no=request.order_no,
    )


@workspace_router.delete(
    "/{workspace_id}",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def delete_workspace(
    auth_info: Request,
    workspace_id: int,
    usecase: WorkspaceUseCase = Depends(Provide[WorkspaceContainer.workspace_service]),
):
    return usecase.delete_workspace(
        user_id=auth_info.user.id, workspace_id=workspace_id
    )
