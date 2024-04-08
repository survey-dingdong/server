from app.project.adapter.output.persistence.repository_adapter import (
    ProjectRepositoryAdapter,
)
from app.project.application.dto import CreateProjectResponseDTO, PatchProjectRequestDTO
from app.project.application.exception import ProjectNotFoundeException
from app.project.domain.command import CreateProjectCommand
from app.project.domain.entity.experiment import (
    ExperimentParticipantTimeSlotRead,
    ExperimentProject,
    ExperimentProjectRead,
    ExperimentTimeSlotRead,
)
from app.project.domain.entity.project import ProjectRead
from app.project.domain.usecase.project import ProjectUseCsae
from app.project.domain.vo.type import ProjectTypeEnum
from core.db import Transactional


class ProjectService(ProjectUseCsae):
    def __init__(self, repository: ProjectRepositoryAdapter) -> None:
        self.repository = repository

    async def get_project_list(
        self,
        workspace_id: int,
        project_type: ProjectTypeEnum,
        page: int,
        size: int,
    ) -> list[ProjectRead]:
        return await self.repository.get_projects(
            workspace_id=workspace_id,
            project_type=project_type,
            page=page,
            size=size,
        )

    async def get_project(
        self,
        project_id: int,
        project_type: ProjectTypeEnum,
    ) -> ExperimentProjectRead | None:
        project = await self.repository.get_project_by_id(
            project_id=project_id,
            project_type=project_type,
        )
        if project is None:
            return None

        time_slots = [
            ExperimentTimeSlotRead(
                id=time_slot.id,
                start_time=time_slot.start_time,
                end_time=time_slot.end_time,
                max_participants=time_slot.max_participants,
            )
            for time_slot in project.experiment_time_slots
        ]

        return ExperimentProjectRead(
            id=project.id,
            title=project.title,
            description=project.description,
            is_public=project.is_public,
            start_date=project.start_date,
            end_date=project.end_date,
            excluded_dates=project.excluded_dates,
            time_slots=time_slots,
            experiment_type=project.experiment_type,
            location=project.location,
            participant_code=project.participant_code,
            created_at=project.created_at,
            updated_at=project.updated_at,
        )

    @Transactional()
    async def create_project(
        self, command: CreateProjectCommand
    ) -> CreateProjectResponseDTO:
        if command.project_type == ProjectTypeEnum.EXPERIMENT:
            project = ExperimentProject.create(
                workspace_id=command.workspace_id, title=command.title
            )
        project = await self.repository.save(project=project, auto_flush=True)
        return CreateProjectResponseDTO(id=project.id)

    @Transactional()
    async def update_project(
        self,
        project_id: int,
        project_type: ProjectTypeEnum,
        project_dto: PatchProjectRequestDTO,
    ) -> None:
        project = await self.repository.get_project_by_id(
            project_id=project_id,
            project_type=project_type,
        )
        if project is None:
            raise ProjectNotFoundeException

        for column, value in project_dto.model_dump(exclude_unset=True).items():
            setattr(project, column, value)

    @Transactional()
    async def delete_project(
        self,
        project_id: int,
        project_type: ProjectTypeEnum,
    ) -> None:
        project = await self.repository.get_project_by_id(
            project_type=project_type,
            project_id=project_id,
        )

        if project is None:
            raise ProjectNotFoundeException

        project.is_deleted = True

    async def get_project_participant_list(
        self,
        project_id: int,
        project_type: ProjectTypeEnum,
        page: int,
        size: int,
    ) -> list[ExperimentParticipantTimeSlotRead]:
        return await self.repository.get_project_participants(
            project_id=project_id,
            project_type=project_type,
            page=page,
            size=size,
        )

    @Transactional()
    async def delete_project_participant(
        self,
        participant_id: int,
        project_type: ProjectTypeEnum,
    ) -> None:
        project_participant = await self.repository.get_project_participant_by_id(
            participant_id=participant_id,
            project_type=project_type,
        )

        if project_participant is None:
            raise ProjectNotFoundeException

        project_participant.is_deleted = True
