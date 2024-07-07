from app.project.application.dto import ExperimentTimeslotDTO
from app.project.domain.entity.experiment import (
    ExperimentParticipantTimeslot,
    ExperimentParticipantTimeslotRead,
    ExperimentProject,
    ExperimentTimeslot,
)
from app.project.domain.repository.project import ProjectRepo
from app.project.domain.vo import ProjectTypeEnum


class ProjectRepositoryAdapter:
    def __init__(self, repository: ProjectRepo) -> None:
        self.repository = repository

    async def get_projects(
        self,
        workspace_id: int,
        project_type: ProjectTypeEnum,
        filter_title: str | None,
        page: int,
        size: int,
    ) -> list[ExperimentProject]:
        return await self.repository.get_projects(
            workspace_id=workspace_id,
            project_type=project_type,
            filter_title=filter_title,
            page=page,
            size=size,
        )

    async def get_project_by_id(
        self,
        project_id: int,
        project_type: ProjectTypeEnum,
    ) -> ExperimentProject | None:
        return await self.repository.get_project_by_id(
            project_id=project_id,
            project_type=project_type,
        )

    async def get_project_timeslot(
        self,
        project_id: int,
        timeslot_id: int,
    ) -> ExperimentTimeslot | None:
        return await self.repository.get_project_timeslot(
            project_id=project_id,
            timeslot_id=timeslot_id,
        )

    async def get_project_participants(
        self,
        project_id: int,
        project_type: ProjectTypeEnum,
        page: int,
        size: int,
    ) -> list[ExperimentParticipantTimeslotRead]:
        project_participants: list[
            ExperimentParticipantTimeslot
        ] = await self.repository.get_project_participants(
            project_id=project_id,
            project_type=project_type,
            page=page,
            size=size,
        )
        return [
            ExperimentParticipantTimeslotRead(**project_participant)
            for project_participant in project_participants
        ]

    async def get_project_participant_by_id(
        self,
        project_id: int,
        participant_id: int,
        project_type: ProjectTypeEnum,
    ) -> ExperimentParticipantTimeslot | None:
        return await self.repository.get_project_participant_by_id(
            project_id=project_id,
            participant_id=participant_id,
            project_type=project_type,
        )

    async def update_timeslots(
        self,
        project: ExperimentProject,
        experiment_timeslots: list[ExperimentTimeslotDTO],
    ) -> None:
        await self.update_timeslots(
            project=project, experiment_timeslots=experiment_timeslots
        )

    async def save(
        self,
        project: ExperimentProject | ExperimentTimeslot,
        auto_flush: bool = False,
    ) -> ExperimentProject | ExperimentTimeslot:
        return await self.repository.save(
            project=project,
            auto_flush=auto_flush,
        )
