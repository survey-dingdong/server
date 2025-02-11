from abc import ABC, abstractmethod

from app.project.application.dto import (
    CreateProjectResponseDTO,
    GetExperimentParticipantsResponseDTO,
    GetProjectListResponseDTO,
    GetProjectResponseDTO,
    UpdateProjectRequestDTO,
)
from app.project.domain.vo import ExperimentAttendanceStatusTypeEnum


class ProjectUseCsae(ABC):
    @abstractmethod
    async def create_project(
        self, workspace_id: int, title: str
    ) -> CreateProjectResponseDTO:
        """Create project"""

    @abstractmethod
    async def get_project_list(
        self,
        workspace_id: int,
        filter_title: str | None,
        page: int,
        size: int,
    ) -> list[GetProjectListResponseDTO]:
        """Get project list"""

    @abstractmethod
    async def get_project(
        self,
        user_id: int,
        project_id: int,
    ) -> GetProjectResponseDTO:
        """Get experiment project"""

    @abstractmethod
    async def put_project(
        self,
        user_id: int,
        project_id: int,
        project_dto: UpdateProjectRequestDTO,
    ) -> None:
        """Update project"""

    @abstractmethod
    async def delete_project(
        self,
        user_id: int,
        project_id: int,
    ) -> None:
        """Delete project"""

    @abstractmethod
    async def get_project_participant_list(
        self,
        user_id: int,
        project_id: int,
        page: int,
        size: int,
    ) -> list[GetExperimentParticipantsResponseDTO]:
        """Get project participant list"""

    @abstractmethod
    async def update_project_participant_status(
        self,
        user_id: int,
        project_id: int,
        participant_id: int,
        attendance_status: ExperimentAttendanceStatusTypeEnum,
    ) -> None:
        """Update project participant status"""

    @abstractmethod
    async def delete_project_participant(
        self,
        user_id: int,
        project_id: int,
        participant_id: int,
    ) -> None:
        """Delete project paticipant"""
