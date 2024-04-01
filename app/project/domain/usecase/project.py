from abc import ABC, abstractmethod

from app.project.application.dto import CreateProjectResponseDTO, PatchProjectRequestDTO
from app.project.domain.entity.experiment import ExperimentProject
from app.project.domain.entity.project import ProjectRead
from app.project.domain.vo.type import ProjectTypeEnum


class ProjectUseCsae(ABC):
    @abstractmethod
    async def get_project_list(
        self,
        workspace_id: int,
        project_type: ProjectTypeEnum,
    ) -> list[ProjectRead]:
        """Get project list"""

    @abstractmethod
    async def get_project(
        self,
        workspace_id: int,
        project_id: int,
        project_type: ProjectTypeEnum,
    ) -> ExperimentProject | None:
        """Get experiment project"""

    @abstractmethod
    async def create_project(self) -> CreateProjectResponseDTO:
        """Create project"""

    @abstractmethod
    async def update_project(
        self,
        workspace_id: int,
        project_id: int,
        project_type: ProjectTypeEnum,
        project_dto: PatchProjectRequestDTO,
    ) -> None:
        """Update project"""

    @abstractmethod
    async def delete_project(
        self,
        workspace_id: int,
        project_id: int,
        project_type: ProjectTypeEnum,
    ) -> None:
        """Delete project"""
