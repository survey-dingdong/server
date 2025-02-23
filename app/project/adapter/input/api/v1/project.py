from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Request, status

from app.project.adapter.input.api.v1.request import (
    CreateProjectRequest,
    GetProjectListRequest,
)
from app.project.application.dto import (
    CreateProjectResponseDTO,
    GetExperimentParticipantsResponseDTO,
    GetProjectListResponseDTO,
    GetProjectResponseDTO,
    UpdateProjectRequestDTO,
)
from app.project.container import ProjectContainer
from app.project.domain.usecase.project import ProjectUseCsae
from app.project.domain.vo import ExperimentAttendanceStatusTypeEnum
from app.workspace.container import WorkspaceContainer
from app.workspace.domain.usecase.workspace import WorkspaceUseCase
from core.fastapi.dependencies import IsResearcher, PermissionDependency

project_router = APIRouter()


@project_router.get(
    "/workspaces/{workspace_id}/projects",
    tags=["Workspace"],
    response_model=list[GetProjectListResponseDTO],
    dependencies=[Depends(PermissionDependency([IsResearcher]))],
)
@inject
async def get_project_list(
    auth_info: Request,
    workspace_id: int,
    request: GetProjectListRequest = Depends(),
    page: int = Query(default=1, ge=1, le=1_000),
    size: int = Query(default=10, ge=1, le=10),
    workspace_usecase: WorkspaceUseCase = Depends(
        Provide[WorkspaceContainer.workspace_service]
    ),
    project_usecase: ProjectUseCsae = Depends(
        Provide[ProjectContainer.project_service]
    ),
) -> list[GetProjectListResponseDTO]:
    workspace = await workspace_usecase.get_workspace_by_id(
        user_id=auth_info.user.id, workspace_id=workspace_id
    )
    return await project_usecase.get_project_list(
        workspace_id=workspace.id,
        filter_title=request.filter_title,
        page=page,
        size=size,
    )


@project_router.post(
    "/workspaces/{workspace_id}/projects",
    tags=["Workspace"],
    response_model=CreateProjectResponseDTO,
    dependencies=[Depends(PermissionDependency([IsResearcher]))],
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_project(
    auth_info: Request,
    workspace_id: int,
    request: CreateProjectRequest,
    workspace_usecase: WorkspaceUseCase = Depends(
        Provide[WorkspaceContainer.workspace_service]
    ),
    project_usecase: ProjectUseCsae = Depends(
        Provide[ProjectContainer.project_service]
    ),
) -> CreateProjectResponseDTO:
    workspace = await workspace_usecase.get_workspace_by_id(
        user_id=auth_info.user.id, workspace_id=workspace_id
    )
    return await project_usecase.create_project(
        workspace_id=workspace.id, title=request.title
    )


@project_router.get(
    "/projects/{project_id}",
    tags=["Project"],
    response_model=GetProjectResponseDTO,
    dependencies=[Depends(PermissionDependency([IsResearcher]))],
)
@inject
async def get_project(
    auth_info: Request,
    project_id: int,
    project_usecase: ProjectUseCsae = Depends(
        Provide[ProjectContainer.project_service]
    ),
) -> GetProjectResponseDTO:
    return await project_usecase.get_project(
        user_id=auth_info.user.id,
        project_id=project_id,
    )


@project_router.put(
    "/projects/{project_id}",
    tags=["Project"],
    dependencies=[Depends(PermissionDependency([IsResearcher]))],
)
@inject
async def put_project(
    auth_info: Request,
    project_id: int,
    request: UpdateProjectRequestDTO,
    project_usecase: ProjectUseCsae = Depends(
        Provide[ProjectContainer.project_service]
    ),
) -> None:
    await project_usecase.put_project(
        user_id=auth_info.user.id,
        project_id=project_id,
        project_dto=request,
    )


@project_router.delete(
    "/projects/{project_id}",
    tags=["Project"],
    dependencies=[Depends(PermissionDependency([IsResearcher]))],
)
@inject
async def delete_project(
    auth_info: Request,
    project_id: int,
    project_usecase: ProjectUseCsae = Depends(
        Provide[ProjectContainer.project_service]
    ),
) -> None:
    await project_usecase.delete_project(
        user_id=auth_info.user.id,
        project_id=project_id,
    )


@project_router.get(
    "/projects/{project_id}/participants",
    tags=["Project"],
    response_model=list[GetExperimentParticipantsResponseDTO],
    dependencies=[Depends(PermissionDependency([IsResearcher]))],
)
@inject
async def get_project_participant_list(
    auth_info: Request,
    project_id: int,
    page: int = Query(default=1, ge=1, le=1_000),
    size: int = Query(default=10, ge=1, le=10),
    project_usecase: ProjectUseCsae = Depends(
        Provide[ProjectContainer.project_service]
    ),
) -> list[GetExperimentParticipantsResponseDTO]:
    return await project_usecase.get_project_participant_list(
        user_id=auth_info.user.id,
        project_id=project_id,
        page=page,
        size=size,
    )


@project_router.patch(
    "/projects/{project_id}/participants/{participant_id}",
    tags=["Project"],
    dependencies=[Depends(PermissionDependency([IsResearcher]))],
)
@inject
async def update_project_participant_status(
    auth_info: Request,
    project_id: int,
    participant_id: int,
    attendance_status: ExperimentAttendanceStatusTypeEnum,
    project_usecase: ProjectUseCsae = Depends(
        Provide[ProjectContainer.project_service]
    ),
) -> None:
    await project_usecase.update_project_participant_status(
        user_id=auth_info.user.id,
        project_id=project_id,
        participant_id=participant_id,
        attendance_status=attendance_status,
    )


@project_router.delete(
    "/projects/{project_id}/participants/{participant_id}",
    tags=["Project"],
    dependencies=[Depends(PermissionDependency([IsResearcher]))],
)
@inject
async def delete_project_participant(
    auth_info: Request,
    project_id: int,
    participant_id: int,
    project_usecase: ProjectUseCsae = Depends(
        Provide[ProjectContainer.project_service]
    ),
) -> None:
    await project_usecase.delete_project_participant(
        user_id=auth_info.user.id,
        project_id=project_id,
        participant_id=participant_id,
    )
