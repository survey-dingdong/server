from app.project.domain.entity.experiment import (
    ExperimentParticipantTimeSlot,
    ExperimentParticipantTimeSlotRead,
    ExperimentProject,
)
from app.project.domain.entity.project import ProjectRead
from app.project.domain.repository.project import ProjectRepo
from app.project.domain.vo.type import ProjectTypeEnum


class ProjectRepositoryAdapter:
    def __init__(self, repository: ProjectRepo) -> None:
        self.repository = repository

    async def get_projects(
        self,
        workspace_id: int,
        project_type: ProjectTypeEnum,
        page: int,
        size: int,
    ) -> list[ProjectRead]:
        projects: list[ExperimentProject] = await self.repository.get_projects(
            workspace_id=workspace_id,
            project_type=project_type,
            page=page,
            size=size,
        )
        return [ProjectRead.model_validate(project) for project in projects]

    async def get_project_by_id(
        self,
        project_id: int,
        project_type: ProjectTypeEnum,
    ) -> ExperimentProject | None:
        return await self.repository.get_project_by_id(
            project_id=project_id,
            project_type=project_type,
        )

    async def get_project_participants(
        self,
        project_id: int,
        project_type: ProjectTypeEnum,
        page: int,
        size: int,
    ) -> list[ExperimentParticipantTimeSlotRead]:
        project_participants: list[
            ExperimentParticipantTimeSlot
        ] = await self.repository.get_project_participants(
            project_id=project_id,
            project_type=project_type,
            page=page,
            size=size,
        )
        return [
            ExperimentParticipantTimeSlotRead.model_validate(
                id=project_participant.id,
                username=project_participant.user.username,
                reserved_date=project_participant.reserved_date,
                attendance_status=project_participant.attendance_status,
                created_at=project_participant.created_at,
                updated_at=project_participant.updated_at,
            )
            for project_participant in project_participants
        ]

    async def get_project_participant_by_id(
        self,
        project_id: int,
        participant_id: int,
        project_type: ProjectTypeEnum,
    ) -> ExperimentParticipantTimeSlot | None:
        return await self.repository.get_project_participant_by_id(
            project_id=project_id,
            participant_id=participant_id,
            project_type=project_type,
        )

    async def save(
        self,
        project: ExperimentProject,
        auto_flush: bool,
    ) -> ExperimentProject:
        return await self.repository.save(
            project=project,
            auto_flush=auto_flush,
        )
