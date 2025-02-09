from abc import ABC, abstractmethod

from app.project.domain.entity.project import (
    ExperimentParticipantTimeslot,
    ExperimentProject,
    ExperimentTimeslot,
)
from app.project.domain.vo import ProjectTypeEnum


class ProjectRepo(ABC):
    @abstractmethod
    async def get_projects(
        self,
        workspace_id: int,
        filter_title: str | None,
        page: int,
        size: int,
    ) -> list[ExperimentProject]:
        """Get project list"""

    @abstractmethod
    async def get_project_by_id(
        self,
        project_id: int,
    ) -> ExperimentProject | None:
        """Get project by id"""

    @abstractmethod
    async def get_project_timeslots(
        self,
        project_id: int,
    ) -> list[ExperimentTimeslot]:
        """Get project timeslot list"""

    @abstractmethod
    async def get_project_timeslot(
        self,
        project_id: int,
        timeslot_id: int,
    ) -> ExperimentTimeslot | None:
        """Get project timeslot by id"""

    @abstractmethod
    async def get_project_participants(
        self,
        project_id: int,
        project_type: ProjectTypeEnum,
        page: int,
        size: int,
    ) -> list[ExperimentParticipantTimeslot]:
        """Get project participant list"""

    @abstractmethod
    async def get_project_participant_by_id(
        self,
        project_id: int,
        participant_id: int,
        project_type: ProjectTypeEnum,
    ) -> ExperimentParticipantTimeslot | None:
        """Get project participant by id"""

    @abstractmethod
    async def add(
        self,
        project: ExperimentProject | ExperimentTimeslot,
        auto_flush: bool,
    ) -> ExperimentProject:
        """Save project"""
