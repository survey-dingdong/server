from typing import cast

import sqlalchemy.dialects.mysql as mysql_dialect
from sqlalchemy import and_, func, select
from sqlalchemy.orm import contains_eager, joinedload

from app.project.application.dto import UpdateProjectRequestDTO
from app.project.domain.entity.project import (
    ExperimentParticipantTimeslot,
    ExperimentProject,
    ExperimentTimeslot,
)
from app.project.domain.repository.project import ProjectRepo
from core.db.session import session


class ProjectSQLAlchemyRepo(ProjectRepo):
    async def get_projects(
        self,
        workspace_id: int,
        filter_title: str | None,
        page: int,
        size: int,
    ) -> list[ExperimentProject]:
        query = (
            select(ExperimentProject)
            .where(
                and_(
                    ExperimentProject.workspace_id == workspace_id,
                    ~ExperimentProject.is_deleted,
                )
            )
            .order_by(ExperimentProject.created_at.desc())
        )

        if filter_title is not None:
            query = query.where(ExperimentProject.title.ilike(f"{filter_title}%"))

        query = query.offset((page - 1) * size).limit(size)
        result = await session.execute(query)
        return cast(list[ExperimentProject], result.scalars().all())

    async def get_project_by_id(self, project_id: int) -> ExperimentProject | None:
        query = (
            select(ExperimentProject)
            .options(joinedload(ExperimentProject.workspace))
            .where(
                and_(
                    ExperimentProject.id == project_id,
                    ~ExperimentProject.is_deleted,
                ),
            )
        )

        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def get_project_timeslots(
        self,
        project_id: int,
    ) -> list[ExperimentTimeslot]:
        query = select(ExperimentTimeslot).where(
            ExperimentTimeslot.experiment_project_id == project_id,
        )

        result = await session.execute(query)
        return cast(list[ExperimentTimeslot], result.scalars().all())

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
        return result.scalar_one_or_none()

    async def upsert_project_timeslots(
        self,
        project_id: int,
        experiment_timeslots: list[UpdateProjectRequestDTO.ExperimentTimeslot],
    ) -> None:
        insert_stmt = mysql_dialect.insert(ExperimentTimeslot).values(
            [
                {
                    "id": experiment_timeslot.id,
                    "experiment_project_id": project_id,
                    "start_time": experiment_timeslot.start_time,
                    "end_time": experiment_timeslot.end_time,
                    "max_participants": experiment_timeslot.max_participants,
                    "created_at": func.current_timestamp(),
                }
                for experiment_timeslot in experiment_timeslots
            ]
        )
        await session.execute(
            insert_stmt.on_duplicate_key_update(
                {
                    "start_time": insert_stmt.inserted.start_time,
                    "end_time": insert_stmt.inserted.end_time,
                    "max_participants": insert_stmt.inserted.max_participants,
                    "updated_at": func.current_timestamp(),
                }
            )
        )

    async def get_project_participants(
        self,
        project_id: int,
        page: int,
        size: int,
    ) -> list[ExperimentParticipantTimeslot]:
        query = (
            select(ExperimentParticipantTimeslot)
            .options(
                joinedload(ExperimentParticipantTimeslot.user),
                contains_eager(ExperimentParticipantTimeslot.experiment_timeslot),
            )
            .join(
                ExperimentTimeslot,
                ExperimentParticipantTimeslot.experiment_timeslot_id
                == ExperimentTimeslot.id,
            )
            .where(
                and_(
                    ExperimentTimeslot.experiment_project_id == project_id,
                    ~ExperimentParticipantTimeslot.is_deleted,
                ),
            )
            .order_by(
                ExperimentParticipantTimeslot.experiment_date,
                ExperimentTimeslot.start_time,
            )
        )
        query = query.offset((page - 1) * size).limit(size)
        result = await session.execute(query)
        return cast(list[ExperimentParticipantTimeslot], result.all())

    async def get_project_participant_by_id(
        self, project_id: int, participant_id: int
    ) -> ExperimentParticipantTimeslot | None:
        query = (
            select(ExperimentParticipantTimeslot)
            .join(
                ExperimentTimeslot,
                ExperimentParticipantTimeslot.experiment_timeslot_id
                == ExperimentTimeslot.id,
            )
            .where(
                and_(
                    ExperimentTimeslot.experiment_project_id == project_id,
                    ExperimentParticipantTimeslot.id == participant_id,
                    ~ExperimentParticipantTimeslot.is_deleted,
                ),
            )
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def add(
        self, project: ExperimentProject | ExperimentTimeslot, auto_flush: bool
    ) -> ExperimentProject:
        session.add(project)
        if auto_flush:
            await session.flush()
        return cast(ExperimentProject, project)
