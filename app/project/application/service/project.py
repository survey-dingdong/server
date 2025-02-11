from typing import cast

from app.project.adapter.output.persistence.repository_adapter import (
    ProjectRepositoryAdapter,
)
from app.project.application.dto import (
    CreateProjectResponseDTO,
    ExperimentTimeslotDTO,
    GetExperimentParticipantsResponseDTO,
    GetProjectListResponseDTO,
    GetProjectResponseDTO,
    UpdateProjectRequestDTO,
)
from app.project.application.exception import (
    ParticipantNotFoundException,
    ProjectAccessDeniedException,
    ProjectNotFoundException,
)
from app.project.domain.entity.project import ExperimentProject
from app.project.domain.usecase.project import ProjectUseCsae
from app.project.domain.vo import ExperimentAttendanceStatusTypeEnum
from core.db import Transactional


class ProjectService(ProjectUseCsae):
    def __init__(
        self,
        repository: ProjectRepositoryAdapter,
    ) -> None:
        self.repository = repository

    @Transactional()
    async def create_project(
        self, workspace_id: int, title: str
    ) -> CreateProjectResponseDTO:
        project = ExperimentProject(workspace_id=workspace_id, title=title)

        project = await self.repository.add(project=project, auto_flush=True)

        return CreateProjectResponseDTO(id=project.id)

    async def get_project_list(
        self,
        workspace_id: int,
        filter_title: str | None,
        page: int,
        size: int,
    ) -> list[GetProjectListResponseDTO]:
        projects = await self.repository.get_projects(
            workspace_id=workspace_id,
            filter_title=filter_title,
            page=page,
            size=size,
        )

        return cast(list[GetProjectListResponseDTO], projects)

    async def get_project(
        self,
        user_id: int,
        project_id: int,
    ) -> GetProjectResponseDTO:
        project = await self.repository.get_project_by_id(
            project_id=project_id,
        )

        if project is None:
            raise ProjectNotFoundException

        if project.workspace.user_id != user_id:
            raise ProjectAccessDeniedException

        experiment_timeslots = cast(
            list[ExperimentTimeslotDTO],
            await self.repository.get_project_timeslots(project.id),
        )

        return GetProjectResponseDTO(
            id=project.id,
            title=project.title,
            description=project.description,
            is_public=project.is_public,
            start_date=project.start_date,
            end_date=project.end_date,
            excluded_dates=project.excluded_dates,
            experiment_timeslots=experiment_timeslots,
            max_participants=project.max_participants,
            experiment_type=project.experiment_type,
            location=project.location,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )

    @Transactional()
    async def put_project(
        self,
        user_id: int,
        project_id: int,
        project_dto: UpdateProjectRequestDTO,
    ) -> None:
        project = await self.repository.get_project_by_id(
            project_id=project_id,
        )
        if project is None:
            raise ProjectNotFoundException

        if project.workspace.user_id != user_id:
            raise ProjectAccessDeniedException

        for column, value in project_dto.model_dump(
            mode="json", exclude={"experiment_timeslots"}
        ).items():
            setattr(project, column, value)

        await self.repository.upsert_project_timeslots(
            project_id=project.id,
            experiment_timeslots=project_dto.experiment_timeslots,
        )

    @Transactional()
    async def delete_project(
        self,
        user_id: int,
        project_id: int,
    ) -> None:
        project = await self.repository.get_project_by_id(
            project_id=project_id,
        )

        if project is None:
            raise ProjectNotFoundException

        if project.workspace.user_id != user_id:
            raise ProjectAccessDeniedException

        project.is_deleted = True

    async def get_project_participant_list(
        self,
        user_id: int,
        project_id: int,
        page: int,
        size: int,
    ) -> list[GetExperimentParticipantsResponseDTO]:
        project = await self.repository.get_project_by_id(
            project_id=project_id,
        )

        if project is None:
            raise ProjectNotFoundException

        if project.workspace.user_id != user_id:
            raise ProjectAccessDeniedException

        project_participants = await self.repository.get_project_participants(
            project_id=project.id,
            page=page,
            size=size,
        )

        return cast(list[GetExperimentParticipantsResponseDTO], project_participants)

    @Transactional()
    async def update_project_participant_status(
        self,
        user_id: int,
        project_id: int,
        participant_id: int,
        attendance_status: ExperimentAttendanceStatusTypeEnum,
    ) -> None:
        project = await self.repository.get_project_by_id(
            project_id=project_id,
        )

        if project is None:
            raise ProjectNotFoundException

        if project.workspace.user_id != user_id:
            raise ProjectAccessDeniedException

        project_participant = await self.repository.get_project_participant_by_id(
            project_id=project.id,
            participant_id=participant_id,
        )

        if project_participant is None:
            raise ParticipantNotFoundException

        project_participant.attendance_status = attendance_status

    @Transactional()
    async def delete_project_participant(
        self,
        user_id: int,
        project_id: int,
        participant_id: int,
    ) -> None:
        project = await self.repository.get_project_by_id(
            project_id=project_id,
        )

        if project is None:
            raise ProjectNotFoundException

        if project.workspace.user_id != user_id:
            raise ProjectAccessDeniedException

        project_participant = await self.repository.get_project_participant_by_id(
            project_id=project.id,
            participant_id=participant_id,
        )

        if project_participant is None:
            raise ParticipantNotFoundException

        project_participant.is_deleted = True
