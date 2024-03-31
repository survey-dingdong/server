from app.project.domain.entity.experiment import ExperimentProject
from app.project.domain.entity.project import ProjectRead
from app.project.domain.repository.project import ProjectRepo
from app.project.domain.vo.type import ProjectTypeEnum


class ProjectRepositoryAdapter:
    def __init__(self, project_repo: ProjectRepo) -> None:
        self.project_repo = project_repo

    async def get_projects(
        self,
        workspace_id: int,
        filter_project_type: ProjectTypeEnum,
    ) -> list[ProjectRead]:
        projects: list[ExperimentProject] = await self.project_repo.get_projects(
            workspace_id=workspace_id, filter_project_type=filter_project_type
        )
        return [ProjectRead.model_validate(project) for project in projects]

    async def get_project_by_id(
        self,
        workspace_id: int,
        project_id: int,
        filter_project_type: ProjectTypeEnum,
    ) -> ExperimentProject | None:
        return await self.project_repo.get_project_by_id(
            workspace_id=workspace_id,
            project_id=project_id,
            filter_project_type=filter_project_type,
        )

    async def delete(
        self,
        workspace_id: int,
        project_id: int,
        filter_project_type: ProjectTypeEnum,
    ):
        await self.project_repo.delete(
            workspace_id=workspace_id,
            project_id=project_id,
            filter_project_type=filter_project_type,
        )

    async def save(
        self,
        project: ExperimentProject,
        auto_flush: bool,
    ) -> ExperimentProject:
        return await self.project_repo.save(
            project=project,
            auto_flush=auto_flush,
        )
