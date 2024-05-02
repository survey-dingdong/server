from typing import Any

from sqlalchemy import and_, select

from app.project.domain.entity.experiment import (
    ExperimentParticipantTimeSlot,
    ExperimentProject,
    ExperimentTimeSlot,
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

    async def get_project_participants(
        self,
        project_id: int,
        project_type: ProjectTypeEnum,
        page: int,
        size: int,
    ) -> list[ExperimentParticipantTimeSlot]:
        if project_type == ProjectTypeEnum.EXPERIMENT:
            participant_time_slot = ExperimentParticipantTimeSlot
        else:
            return []

        query = (
            select(participant_time_slot, ExperimentTimeSlot)
            .join(ExperimentParticipantTimeSlot.experiment_time_slot)
            .join(ExperimentTimeSlot.experiment_project)
            .where(
                and_(
                    ExperimentTimeSlot.experiment_project_id == project_id,
                    participant_time_slot.is_deleted == False,  # noqa: E712
                ),
            )
            .order_by(
                ExperimentParticipantTimeSlot.experiment_date,
                ExperimentTimeSlot.start_time,
            )
        )
        query = query.offset((page - 1) * size).limit(size)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_project_participant_by_id(
        self, project_id: int, participant_id: int, project_type: ProjectTypeEnum
    ) -> ExperimentParticipantTimeSlot | None:
        if project_type == ProjectTypeEnum.EXPERIMENT:
            participant_time_slot = ExperimentParticipantTimeSlot
        else:
            return None

        query = select(participant_time_slot).where(
            and_(
                ExperimentParticipantTimeSlot.experiment_time_slot.experiment_project_id
                == project_id,
                ExperimentParticipantTimeSlot.id == participant_id,
                ExperimentParticipantTimeSlot.is_deleted == False,  # noqa: E712
            ),
        )
        result = await session.execute(query)
        return result.scalars().first()

    async def save(
        self, project: ExperimentProject, auto_flush: bool = False
    ) -> ExperimentProject:
        session.add(project)
        if auto_flush:
            await session.flush()
        return project
