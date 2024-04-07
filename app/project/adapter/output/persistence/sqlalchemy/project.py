from typing import Any

from sqlalchemy import and_, select

from app.project.domain.entity.experiment import ExperimentProject
from app.project.domain.repository.project import ProjectRepo
from app.project.domain.vo.type import ProjectTypeEnum
from core.db.session import session


class ProjectSQLAlchemyRepo(ProjectRepo):
    @staticmethod
    def _get_entity_by_project_type(project_type: ProjectTypeEnum) -> Any:
        return {ProjectTypeEnum.EXPERIMENT: ExperimentProject}[project_type]

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

        query = (
            select(project)
            .where(
                and_(ExperimentProject.workspace_id == workspace_id),
                ExperimentProject.is_deleted == False,  # noqa: E712
            )
            .order_by(ExperimentProject.created_at.desc())
        )

        query = query.offset((page - 1) * size).limit(size)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_project_by_id(
        self, project_id: int, project_type: ProjectTypeEnum
    ) -> ExperimentProject | None:
        project: ExperimentProject = ProjectSQLAlchemyRepo._get_entity_by_project_type(
            project_type
        )

        query = (
            select(project)
            .where(
                and_(ExperimentProject.id == project_id),
                ExperimentProject.is_deleted == False,  # noqa: E712
            )
            .order_by(ExperimentProject.created_at.desc())
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
