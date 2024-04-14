from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request

from app.project.adapter.input.api.v1.request import PatchProjectRequest
from app.project.adapter.input.api.v1.response import (
    CreateProjectResponse,
    GetExperimentParticipantResponse,
    GetExperimentProjectResponse,
    ProjectResponse,
)
from app.project.container import ProjectContainer
from app.project.domain.command import CreateProjectCommand
from app.project.domain.usecase.project import ProjectUseCsae
from app.project.domain.vo.type import ProjectTypeEnum
from app.workspace.container import WorkspaceContainer
from app.workspace.domain.usecase.workspace import WorkspaceUseCase
from core.fastapi.dependencies import IsAuthenticated, PermissionDependency

project_router = APIRouter()


@project_router.get(
    "/{workspace_id}/projects",
    response_model=list[ProjectResponse],
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def get_project_list(
    auth_info: Request,
    workspace_id: int,
    project_type: ProjectTypeEnum,
    page: int,
    size: int,
    workspace_usecase: WorkspaceUseCase = Depends(
        Provide[WorkspaceContainer.workspace_service]
    ),
    project_usecase: ProjectUseCsae = Depends(
        Provide[ProjectContainer.project_service]
    ),
):
    workspace = await workspace_usecase.get_workspace_by_id(
        user_id=auth_info.user.id, workspace_id=workspace_id
    )
    return await project_usecase.get_project_list(
        workspace_id=workspace.id, project_type=project_type, page=page, size=size
    )


@project_router.get(
    "/{workspace_id}/projects/{project_id}",
    response_model=GetExperimentProjectResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def get_project(
    auth_info: Request,
    workspace_id: int,
    project_id: int,
    project_type: ProjectTypeEnum,
    workspace_usecase: WorkspaceUseCase = Depends(
        Provide[WorkspaceContainer.workspace_service]
    ),
    project_usecase: ProjectUseCsae = Depends(
        Provide[ProjectContainer.project_service]
    ),
):
    workspace = await workspace_usecase.get_workspace_by_id(
        user_id=auth_info.user.id, workspace_id=workspace_id
    )
    return await project_usecase.get_project(
        workspace_id=workspace.id, project_id=project_id, project_type=project_type
    )


@project_router.post(
    "/{workspace_id}/projects",
    response_model=CreateProjectResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def create_project(
    auth_info: Request,
    workspace_id: int,
    project_type: ProjectTypeEnum,
    workspace_usecase: WorkspaceUseCase = Depends(
        Provide[WorkspaceContainer.workspace_service]
    ),
    project_usecase: ProjectUseCsae = Depends(
        Provide[ProjectContainer.project_service]
    ),
):
    workspace = await workspace_usecase.get_workspace_by_id(
        user_id=auth_info.user.id, workspace_id=workspace_id
    )
    command = CreateProjectCommand(workspace_id=workspace.id, project_type=project_type)
    return await project_usecase.create_project(command=command)


@project_router.patch(
    "/{workspace_id}/projects/{project_id}",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def patch_project(
    auth_info: Request,
    workspace_id: int,
    project_id: int,
    project_type: ProjectTypeEnum,
    request: PatchProjectRequest,
    workspace_usecase: WorkspaceUseCase = Depends(
        Provide[WorkspaceContainer.workspace_service]
    ),
    project_usecase: ProjectUseCsae = Depends(
        Provide[ProjectContainer.project_service]
    ),
):
    workspace = await workspace_usecase.get_workspace_by_id(
        user_id=auth_info.user.id, workspace_id=workspace_id
    )
    return await project_usecase.update_project(
        workspace_id=workspace.id,
        project_id=project_id,
        project_type=project_type,
        project_dto=request,
    )


@project_router.delete(
    "/{workspace_id}/projects/{project_id}",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def delete_project(
    auth_info: Request,
    workspace_id: int,
    project_id: int,
    project_type: ProjectTypeEnum,
    workspace_usecase: WorkspaceUseCase = Depends(
        Provide[WorkspaceContainer.workspace_service]
    ),
    project_usecase: ProjectUseCsae = Depends(
        Provide[ProjectContainer.project_service]
    ),
):
    workspace = await workspace_usecase.get_workspace_by_id(
        user_id=auth_info.user.id, workspace_id=workspace_id
    )
    return await project_usecase.delete_project(
        workspace_id=workspace.id, project_id=project_id, project_type=project_type
    )


@project_router.get(
    "/{workspace_id}/projects/{project_id}/participants",
    response_model=list[GetExperimentParticipantResponse],
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def get_project_participant_list(
    auth_info: Request,
    workspace_id: int,
    project_id: int,
    project_type: ProjectTypeEnum,
    page: int,
    size: int,
    workspace_usecase: WorkspaceUseCase = Depends(
        Provide[WorkspaceContainer.workspace_service]
    ),
    project_usecase: ProjectUseCsae = Depends(
        Provide[ProjectContainer.project_service]
    ),
):
    workspace = await workspace_usecase.get_workspace_by_id(
        user_id=auth_info.user.id, workspace_id=workspace_id
    )
    return await project_usecase.get_project_participant_list(
        workspace_id=workspace.id,
        project_id=project_id,
        project_type=project_type,
        page=page,
        size=size,
    )


@project_router.delete(
    "/{workspace_id}/projects/{project_id}/participants/{participant_id}",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def delete_project_participant(
    auth_info: Request,
    workspace_id: int,
    project_id: int,
    participant_id: int,
    project_type: ProjectTypeEnum,
    workspace_usecase: WorkspaceUseCase = Depends(
        Provide[WorkspaceContainer.workspace_service]
    ),
    project_usecase: ProjectUseCsae = Depends(
        Provide[ProjectContainer.project_service]
    ),
):
    workspace = await workspace_usecase.get_workspace_by_id(
        user_id=auth_info.user.id, workspace_id=workspace_id
    )
    return await project_usecase.delete_project_participant(
        workspace_id=workspace.id,
        project_id=project_id,
        participant_id=participant_id,
        project_type=project_type,
    )
