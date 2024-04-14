from abc import ABC, abstractmethod

from app.project.domain.entity.experiment import (
    ExperimentParticipantTimeSlot,
    ExperimentProject,
)
from app.project.domain.vo.type import ProjectTypeEnum


class ProjectRepo(ABC):
    @abstractmethod
    async def get_projects(
        self,
        workspace_id: int,
        project_type: ProjectTypeEnum,
        page: int,
        size: int,
    ) -> list[ExperimentProject]:
        """Get project list"""

    @abstractmethod
    async def get_project_by_id(
        self,
        project_id: int,
        project_type: ProjectTypeEnum,
    ) -> ExperimentProject | None:
        """Get project by id"""

    @abstractmethod
    async def get_project_participants(
        self,
        project_id: int,
        project_type: ProjectTypeEnum,
        page: int,
        size: int,
    ) -> list[ExperimentParticipantTimeSlot]:
        """Get project participant list"""

    @abstractmethod
    async def get_project_participant_by_id(
        self,
        project_id: int,
        participant_id: int,
        project_type: ProjectTypeEnum,
    ) -> ExperimentParticipantTimeSlot | None:
        """Get project participant by id"""

    @abstractmethod
    async def save(
        self,
        project: ExperimentProject,
        auto_flush: bool,
    ) -> ExperimentProject:
        """Save project"""
