from typing import Any

from sqlalchemy import and_, select

from app.project.domain.entity.experiment import (
    ExperimentParticipantTimeslot,
    ExperimentProject,
    ExperimentTimeslot,
)
from app.project.domain.repository.project import ProjectRepo
from app.project.domain.vo.type import ProjectTypeEnum
from core.db.session import session


class ProjectSQLAlchemyRepo(ProjectRepo):
    @staticmethod
    def _get_entity_by_project_type(project_type: ProjectTypeEnum) -> Any:
        return {ProjectTypeEnum.EXPERIMENT: ExperimentProject}.get(project_type)

    async def get_projects(
        self,
        workspace_id: int,
        project_type: ProjectTypeEnum,
        page: int,
        size: int,
    ) -> list[ExperimentProject]:
        project: ExperimentProject = ProjectSQLAlchemyRepo._get_entity_by_project_type(
            project_type
        )
        if project is None:
            return []

        query = (
            select(project)
            .where(
                and_(
                    ExperimentProject.workspace_id == workspace_id,
                    ExperimentProject.is_deleted == False,  # noqa: E712
                )
            )
            .order_by(ExperimentProject.created_at.desc())
        )

        query = query.offset((page - 1) * size).limit(size)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_project_by_id(
        self, workspace_id: int, project_id: int, project_type: ProjectTypeEnum
    ) -> ExperimentProject | None:
        project: ExperimentProject = ProjectSQLAlchemyRepo._get_entity_by_project_type(
            project_type
        )
        if project is None:
            return None

        query = select(project).where(
            and_(
                ExperimentProject.workspace_id == workspace_id,
                ExperimentProject.id == project_id,
                ExperimentProject.is_deleted == False,  # noqa: E712
            ),
        )

        result = await session.execute(query)
        return result.scalars().first()

    async def get_project_timeslot(
        self,
        project_id: int,
        timeslot_id: int,
    ) -> ExperimentTimeslot | None:
        query = select(ExperimentTimeslot).where(
            and_(
                ExperimentTimeslot.id == timeslot_id,
                ExperimentTimeslot.experiment_project_id == project_id,
            )
        )

        result = await session.execute(query)
        return result.scalars().first()

    async def get_project_participants(
        self,
        project_id: int,
        project_type: ProjectTypeEnum,
        page: int,
        size: int,
    ) -> list[ExperimentParticipantTimeslot]:
        if project_type == ProjectTypeEnum.EXPERIMENT:
            participant_timeslot = ExperimentParticipantTimeslot
        else:
            return []

        query = (
            select(participant_timeslot, ExperimentTimeslot)
            .join(ExperimentParticipantTimeslot.experiment_timeslot)
            .join(ExperimentTimeslot.experiment_project)
            .where(
                and_(
                    ExperimentTimeslot.experiment_project_id == project_id,
                    participant_timeslot.is_deleted == False,  # noqa: E712
                ),
            )
            .order_by(
                ExperimentParticipantTimeslot.experiment_date,
                ExperimentTimeslot.start_time,
            )
        )
        query = query.offset((page - 1) * size).limit(size)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_project_participant_by_id(
        self, project_id: int, participant_id: int, project_type: ProjectTypeEnum
    ) -> ExperimentParticipantTimeslot | None:
        if project_type == ProjectTypeEnum.EXPERIMENT:
            participant_timeslot = ExperimentParticipantTimeslot
        else:
            return None

        query = select(participant_timeslot).where(
            and_(
                ExperimentParticipantTimeslot.experiment_timeslot.experiment_project_id
                == project_id,
                ExperimentParticipantTimeslot.id == participant_id,
                ExperimentParticipantTimeslot.is_deleted == False,  # noqa: E712
            ),
        )
        result = await session.execute(query)
        return result.scalars().first()

    async def save(
        self, project: ExperimentProject | ExperimentTimeslot, auto_flush: bool
    ) -> ExperimentProject | ExperimentTimeslot:
        session.add(project)
        if auto_flush:
            await session.flush()
        return project
