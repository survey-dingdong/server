from app.project.adapter.output.persistence.repository_adapter import (
    ProjectRepositoryAdapter,
)
from app.project.application.dto import CreateProjectResponseDTO
from app.project.application.exception import ProjectNotFoundeException
from app.project.domain.command import CreateProjectCommand
from app.project.domain.entity.experiment import ExperimentProject
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
        filter_project_type: ProjectTypeEnum,
    ) -> list[ProjectRead]:
        return await self.repository.get_projects(
            workspace_id=workspace_id,
            filter_project_type=filter_project_type,
        )

    async def get_project(
        self,
        workspace_id: int,
        project_id: int,
        filter_project_type: ProjectTypeEnum,
    ) -> ExperimentProject | None:
        return await self.repository.get_project_by_id(
            workspace_id=workspace_id,
            project_id=project_id,
            filter_project_type=filter_project_type,
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
        filter_project_type: ProjectTypeEnum,
    ) -> None:
        project = await self.repository.get_project_by_id(
            workspace_id=workspace_id,
            project_id=project_id,
            filter_project_type=filter_project_type,
        )
        if project is None:
            raise ProjectNotFoundeException

        return None

    async def delete_project(
        self,
        workspace_id: int,
        project_id: int,
        filter_project_type: ProjectTypeEnum,
    ) -> None:
        return await self.repository.delete(
            workspace_id=workspace_id,
            project_id=project_id,
            filter_project_type=filter_project_type,
        )
