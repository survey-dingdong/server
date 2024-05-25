from app.project.adapter.output.persistence.repository_adapter import (
    ProjectRepositoryAdapter,
)
from app.project.application.dto import (
    CreateProjectResponseDTO,
    UpdateProjectRequestDTO,
)
from app.project.application.exception import (
    ParticipantAccessDeniedException,
    ParticipantNotFoundException,
    ProjectNotFoundException,
    ProjectTimeslotNotFoundException,
)
from app.project.domain.command import CreateProjectCommand
from app.project.domain.entity.experiment import (
    ExperimentParticipantTimeslotRead,
    ExperimentProject,
    ExperimentProjectRead,
    ExperimentTimeslot,
    ExperimentTimeslotRead,
)
from app.project.domain.entity.project import ProjectRead
from app.project.domain.usecase.project import ProjectUseCsae
from app.project.domain.vo.type import ProjectTypeEnum
from core.db import Transactional


class ProjectService(ProjectUseCsae):
    def __init__(
        self,
        repository: ProjectRepositoryAdapter,
    ) -> None:
        self.repository = repository

    async def get_project_list(
        self,
        workspace_id: int,
        project_type: ProjectTypeEnum,
        page: int,
        size: int,
    ) -> list[ProjectRead]:
        projects = await self.repository.get_projects(
            workspace_id=workspace_id,
            project_type=project_type,
            page=page,
            size=size,
        )

        return [ProjectRead.model_validate(project) for project in projects]

    async def get_project(
        self,
        workspace_id: int,
        project_id: int,
        project_type: ProjectTypeEnum,
    ) -> ExperimentProjectRead:
        project = await self.repository.get_project_by_id(
            workspace_id=workspace_id,
            project_id=project_id,
            project_type=project_type,
        )
        if project is None:
            raise ProjectNotFoundException

        experiment_timeslots = [
            ExperimentTimeslotRead(
                id=time_slot.id,
                start_time=time_slot.start_time,
                end_time=time_slot.end_time,
                max_participants=time_slot.max_participants,
            )
            for time_slot in project.experiment_timeslots
        ]

        return ExperimentProjectRead(
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
        workspace_id: int,
        project_id: int,
        project_type: ProjectTypeEnum,
        project_dto: UpdateProjectRequestDTO,
    ) -> None:
        project = await self.repository.get_project_by_id(
            workspace_id=workspace_id,
            project_id=project_id,
            project_type=project_type,
        )
        if project is None:
            raise ProjectNotFoundException

        for column, value in project_dto.model_dump(
            mode="json", exclude="experiment_timeslots"
        ).items():
            setattr(project, column, value)

        for timeslot_data in project_dto.experiment_timeslots:
            if timeslot_data.id is None:
                new_project_timeslot = ExperimentTimeslot.create(
                    experiment_project_id=project.id,
                    start_time=timeslot_data.start_time,
                    end_time=timeslot_data.end_time,
                    max_participants=timeslot_data.max_participants,
                )
                await self.repository.save(project=new_project_timeslot)
            else:
                project_timeslot = await self.repository.get_project_timeslot(
                    project_id=project.id, timeslot_id=timeslot_data.id
                )
                if project_timeslot is None:
                    raise ProjectTimeslotNotFoundException

                project_timeslot.start_time = timeslot_data.start_time
                project_timeslot.end_time = timeslot_data.end_time
                project_timeslot.max_participants = timeslot_data.max_participants

    @Transactional()
    async def delete_project(
        self,
        workspace_id: int,
        project_id: int,
        project_type: ProjectTypeEnum,
    ) -> None:
        project = await self.repository.get_project_by_id(
            workspace_id=workspace_id,
            project_type=project_type,
            project_id=project_id,
        )

        if project is None:
            raise ProjectNotFoundException

        project.is_deleted = True

    async def get_project_participant_list(
        self,
        workspace_id: int,
        project_id: int,
        project_type: ProjectTypeEnum,
        page: int,
        size: int,
    ) -> list[ExperimentParticipantTimeslotRead]:
        project = await self.repository.get_project_by_id(
            workspace_id=workspace_id,
            project_type=project_type,
            project_id=project_id,
        )

        if project is None:
            raise ProjectNotFoundException

        return await self.repository.get_project_participants(
            project_id=project.id,
            project_type=project_type,
            page=page,
            size=size,
        )

    @Transactional()
    async def delete_project_participant(
        self,
        workspace_id: int,
        project_id: int,
        participant_id: int,
        project_type: ProjectTypeEnum,
    ) -> None:
        project = await self.repository.get_project_by_id(
            workspace_id=workspace_id,
            project_type=project_type,
            project_id=project_id,
        )

        if project is None:
            raise ProjectNotFoundException

        project_participant = await self.repository.get_project_participant_by_id(
            project_id=project.id,
            participant_id=participant_id,
            project_type=project_type,
        )

        if project_participant is None:
            raise ParticipantNotFoundException

        if project_participant.experiment_timeslot.experiment_project_id != project_id:
            raise ParticipantAccessDeniedException

        project_participant.is_deleted = True
