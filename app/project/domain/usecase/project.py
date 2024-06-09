from abc import ABC, abstractmethod

from app.project.application.dto import (
    CreateProjectResponseDTO,
    UpdateProjectRequestDTO,
)
from app.project.domain.command import CreateProjectCommand
from app.project.domain.entity.experiment import (
    ExperimentParticipantTimeslotRead,
    ExperimentProjectRead,
)
from app.project.domain.entity.project import ProjectRead
from app.project.domain.vo import ProjectTypeEnum


class ProjectUseCsae(ABC):
    @abstractmethod
    async def get_project_list(
        self,
        workspace_id: int,
        project_type: ProjectTypeEnum,
        page: int,
        size: int,
    ) -> list[ProjectRead]:
        """Get project list"""

    @abstractmethod
    async def get_project(
        self,
        user_id: int,
        project_id: int,
        project_type: ProjectTypeEnum,
    ) -> ExperimentProjectRead:
        """Get experiment project"""

    @abstractmethod
    async def create_project(
        self, command: CreateProjectCommand
    ) -> CreateProjectResponseDTO:
        """Create project"""

    @abstractmethod
    async def update_project(
        self,
        user_id: int,
        project_id: int,
        project_type: ProjectTypeEnum,
        project_dto: UpdateProjectRequestDTO,
    ) -> None:
        """Update project"""

    @abstractmethod
    async def delete_project(
        self,
        user_id: int,
        project_id: int,
        project_type: ProjectTypeEnum,
    ) -> None:
        """Delete project"""

    @abstractmethod
    async def get_project_participant_list(
        self,
        user_id: int,
        project_id: int,
        project_type: ProjectTypeEnum,
        page: int,
        size: int,
    ) -> list[ExperimentParticipantTimeslotRead]:
        """Get project participant list"""

    @abstractmethod
    async def delete_project_participant(
        self,
        user_id: int,
        project_id: int,
        participant_id: int,
        project_type: ProjectTypeEnum,
    ) -> None:
        """Delete project paticipant"""
