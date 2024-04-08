from abc import ABC, abstractmethod

from app.project.application.dto import CreateProjectResponseDTO, PatchProjectRequestDTO
from app.project.domain.entity.experiment import (
    ExperimentParticipantTimeSlotRead,
    ExperimentProjectRead,
)
from app.project.domain.entity.project import ProjectRead
from app.project.domain.vo.type import ProjectTypeEnum


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
        project_id: int,
        project_type: ProjectTypeEnum,
    ) -> ExperimentProjectRead | None:
        """Get experiment project"""

    @abstractmethod
    async def create_project(self) -> CreateProjectResponseDTO:
        """Create project"""

    @abstractmethod
    async def update_project(
        self,
        project_id: int,
        project_type: ProjectTypeEnum,
        project_dto: PatchProjectRequestDTO,
    ) -> None:
        """Update project"""

    @abstractmethod
    async def delete_project(
        self,
        project_id: int,
        project_type: ProjectTypeEnum,
    ) -> None:
        """Delete project"""

    @abstractmethod
    async def get_project_participant_list(
        self,
        project_id: int,
        project_type: ProjectTypeEnum,
        page: int,
        size: int,
    ) -> list[ExperimentParticipantTimeSlotRead]:
        """Get project participant list"""

    @abstractmethod
    async def delete_project_participant(
        self,
        participant_id: int,
        project_type: ProjectTypeEnum,
    ) -> None:
        """Delete project paticipant"""
