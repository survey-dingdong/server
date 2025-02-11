from app.project.application.dto import ExperimentTimeslotDTO, UpdateProjectRequestDTO
from app.project.domain.entity.project import (
    ExperimentParticipantTimeslot,
    ExperimentProject,
    ExperimentTimeslot,
)
from app.project.domain.repository.project import ProjectRepo


class ProjectRepositoryAdapter:
    def __init__(self, repository: ProjectRepo) -> None:
        self.repository = repository

    async def get_projects(
        self,
        workspace_id: int,
        filter_title: str | None,
        page: int,
        size: int,
    ) -> list[ExperimentProject]:
        return await self.repository.get_projects(
            workspace_id=workspace_id,
            filter_title=filter_title,
            page=page,
            size=size,
        )

    async def get_project_by_id(
        self,
        project_id: int,
    ) -> ExperimentProject | None:
        return await self.repository.get_project_by_id(
            project_id=project_id,
        )

    async def get_project_timeslots(
        self,
        project_id: int,
    ) -> list[ExperimentTimeslot]:
        return await self.repository.get_project_timeslots(
            project_id=project_id,
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

    async def upsert_project_timeslots(
        self,
        project_id: int,
        experiment_timeslots: list[UpdateProjectRequestDTO.ExperimentTimeslot],
    ) -> None:
        await self.repository.upsert_project_timeslots(
            project_id=project_id,
            experiment_timeslots=experiment_timeslots,
        )

    async def get_project_participants(
        self,
        project_id: int,
        page: int,
        size: int,
    ) -> list[ExperimentParticipantTimeslot]:
        return await self.repository.get_project_participants(
            project_id=project_id,
            page=page,
            size=size,
        )

    async def get_project_participant_by_id(
        self,
        project_id: int,
        participant_id: int,
    ) -> ExperimentParticipantTimeslot | None:
        return await self.repository.get_project_participant_by_id(
            project_id=project_id,
            participant_id=participant_id,
        )

    async def update_timeslots(
        self,
        project: ExperimentProject,
        experiment_timeslots: list[ExperimentTimeslotDTO],
    ) -> None:
        await self.update_timeslots(
            project=project, experiment_timeslots=experiment_timeslots
        )

    async def add(
        self,
        project: ExperimentProject | ExperimentTimeslot,
        auto_flush: bool = False,
    ) -> ExperimentProject:
        return await self.repository.add(
            project=project,
            auto_flush=auto_flush,
        )
