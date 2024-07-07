from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Request, status

from app.project.adapter.input.api.v1.request import (
    CreateProjectRequest,
    GetProjectListRequest,
    PutProjectRequest,
)
from app.project.adapter.input.api.v1.response import (
    CreateProjectResponse,
    GetExperimentParticipantResponse,
    GetExperimentProjectResponse,
    GetProjectListResponse,
)
from app.project.container import ProjectContainer
from app.project.domain.command import CreateProjectCommand
from app.project.domain.usecase.project import ProjectUseCsae
from app.project.domain.vo import ProjectTypeEnum
from app.workspace.container import WorkspaceContainer
from app.workspace.domain.usecase.workspace import WorkspaceUseCase
from core.fastapi.dependencies import IsAuthenticated, PermissionDependency

project_router = APIRouter()


@project_router.get(
    "/workspaces/{workspace_id}/projects",
    tags=["Workspace"],
    response_model=list[GetProjectListResponse],
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def get_project_list(
    auth_info: Request,
    workspace_id: int,
    project_type: ProjectTypeEnum,
    request: GetProjectListRequest = Depends(),
    page: int = Query(default=1),
    size: int = Query(default=10),
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
        workspace_id=workspace.id,
        project_type=project_type,
        filter_title=request.filter_title,
        page=page,
        size=size,
    )


@project_router.post(
    "/workspaces/{workspace_id}/projects",
    tags=["Workspace"],
    response_model=CreateProjectResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_project(
    auth_info: Request,
    workspace_id: int,
    project_type: ProjectTypeEnum,
    request: CreateProjectRequest,
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
    command = CreateProjectCommand(
        workspace_id=workspace.id, title=request.title, project_type=project_type
    )
    return await project_usecase.create_project(command=command)


@project_router.get(
    "/projects/{project_id}",
    tags=["Project"],
    response_model=GetExperimentProjectResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def get_project(
    auth_info: Request,
    project_id: int,
    project_type: ProjectTypeEnum,
    project_usecase: ProjectUseCsae = Depends(
        Provide[ProjectContainer.project_service]
    ),
):
    return await project_usecase.get_project(
        user_id=auth_info.user.id,
        project_id=project_id,
        project_type=project_type,
    )


@project_router.put(
    "/projects/{project_id}",
    tags=["Project"],
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def update_project(
    auth_info: Request,
    project_id: int,
    project_type: ProjectTypeEnum,
    request: PutProjectRequest,
    project_usecase: ProjectUseCsae = Depends(
        Provide[ProjectContainer.project_service]
    ),
):
    await project_usecase.update_project(
        user_id=auth_info.user.id,
        project_id=project_id,
        project_type=project_type,
        project_dto=request,
    )


@project_router.delete(
    "/projects/{project_id}",
    tags=["Project"],
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def delete_project(
    auth_info: Request,
    project_id: int,
    project_type: ProjectTypeEnum,
    project_usecase: ProjectUseCsae = Depends(
        Provide[ProjectContainer.project_service]
    ),
):
    await project_usecase.delete_project(
        user_id=auth_info.user.id,
        project_id=project_id,
        project_type=project_type,
    )


@project_router.get(
    "/projects/{project_id}/participants",
    tags=["Project"],
    response_model=list[GetExperimentParticipantResponse],
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def get_project_participant_list(
    auth_info: Request,
    project_id: int,
    project_type: ProjectTypeEnum,
    page: int = Query(default=1),
    size: int = Query(default=10),
    project_usecase: ProjectUseCsae = Depends(
        Provide[ProjectContainer.project_service]
    ),
):
    return await project_usecase.get_project_participant_list(
        user_id=auth_info.user.id,
        project_id=project_id,
        project_type=project_type,
        page=page,
        size=size,
    )


@project_router.delete(
    "/projects/{project_id}/participants/{participant_id}",
    tags=["Project"],
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def delete_project_participant(
    auth_info: Request,
    project_id: int,
    participant_id: int,
    project_type: ProjectTypeEnum,
    project_usecase: ProjectUseCsae = Depends(
        Provide[ProjectContainer.project_service]
    ),
):
    await project_usecase.delete_project_participant(
        user_id=auth_info.user.id,
        project_id=project_id,
        participant_id=participant_id,
        project_type=project_type,
    )
