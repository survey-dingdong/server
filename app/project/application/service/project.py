from app.project.adapter.output.persistence.repository_adapter import (
    ProjectRepositoryAdapter,
)
from app.project.application.dto import CreateProjectResponseDTO, PatchProjectRequestDTO
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
    ) -> ExperimentProject | None:
        return await self.repository.get_project_by_id(
            project_id=project_id,
            project_type=project_type,
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
