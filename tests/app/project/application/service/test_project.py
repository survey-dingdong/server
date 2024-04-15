from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.project.adapter.output.persistence.repository_adapter import (
    ProjectRepositoryAdapter,
)
from app.project.application.dto import PatchProjectRequestDTO
from app.project.application.exception import (
    ProjectAccessDeniedException,
    ProjectNotFoundException,
)
from app.project.application.service.project import ProjectService
from app.project.domain.command import CreateProjectCommand
from app.project.domain.entity.experiment import ExperimentParticipantTimeSlotRead
from app.project.domain.entity.project import ProjectRead
from app.project.domain.vo.type import (
    ExperimentAttendanceStatus,
    ExperimentTypeEnum,
    ProjectTypeEnum,
)
from tests.support.project_fixture import (
    make_experiment_project,
    make_experiment_project_participant,
)

repository_mock = AsyncMock(spec=ProjectRepositoryAdapter)
project_service = ProjectService(repository=repository_mock)


@pytest.mark.asyncio
async def test_get_project_list():
    # Given
    project = ProjectRead(
        id=1,
        workspace_id=1,
        title="project",
        is_public=False,
        joined_participants=0,
        max_participants=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    repository_mock.get_projects.return_value = [project]
    project_service.repository = repository_mock

    # When
    sut = await project_service.get_project_list(
        workspace_id=1,
        project_type=ProjectTypeEnum.EXPERIMENT,
        page=1,
        size=12,
    )

    # Then
    assert len(sut) == 1
    result = sut[0]
    assert result.id == project.id
    assert result.workspace_id == project.workspace_id
    assert result.title == project.title


@pytest.mark.asyncio
async def test_get_project_not_exist():
    # Given
    repository_mock.get_project_by_id.return_value = None
    project_service.repository = repository_mock

    # When
    # When, Then
    with pytest.raises(ProjectNotFoundException):
        await project_service.get_project(
            workspace_id=1,
            project_id=2,
            project_type=ProjectTypeEnum.EXPERIMENT,
        )


@pytest.mark.asyncio
async def test_get_project_access_denied():
    # Given
    project = make_experiment_project(id=1)
    repository_mock.get_project_by_id.return_value = project
    project_service.repository = repository_mock

    # When
    # When, Then
    with pytest.raises(ProjectAccessDeniedException):
        await project_service.get_project(
            workspace_id=2,
            project_id=2,
            project_type=ProjectTypeEnum.EXPERIMENT,
        )


@pytest.mark.asyncio
async def test_get_project_by_id():
    # Given
    project = make_experiment_project(id=1)
    repository_mock.get_project_by_id.return_value = project
    project_service.repository = repository_mock

    # When
    sut = await project_service.get_project(
        workspace_id=1,
        project_id=project.id,
        project_type=ProjectTypeEnum.EXPERIMENT,
    )
    assert sut.id == 1


@pytest.mark.asyncio
async def test_create_project():
    # Given
    command = CreateProjectCommand(
        workspace_id=1,
        title="project",
        project_type=ProjectTypeEnum.EXPERIMENT,
    )

    # When
    sut = await project_service.create_project(command=command)

    # Then
    assert sut.id == 1


@pytest.mark.asyncio
async def test_update_project_not_exist():
    # Given
    repository_mock.get_project_by_id.return_value = None
    project_service.repository = repository_mock

    project_dto = PatchProjectRequestDTO(title="Chnage title")

    # When, Then
    with pytest.raises(ProjectNotFoundException):
        await project_service.update_project(
            workspace_id=1,
            project_id=2,
            project_type=ProjectTypeEnum.EXPERIMENT,
            project_dto=project_dto,
        )


@pytest.mark.asyncio
async def test_update_project_access_denied():
    # Given
    project = make_experiment_project(id=1)
    repository_mock.get_project_by_id.return_value = project
    project_service.repository = repository_mock

    project_dto = PatchProjectRequestDTO(title="Chnage title")

    # When, Then
    with pytest.raises(ProjectAccessDeniedException):
        await project_service.update_project(
            workspace_id=2,
            project_id=2,
            project_type=ProjectTypeEnum.EXPERIMENT,
            project_dto=project_dto,
        )


@pytest.mark.asyncio
async def test_updated_project():
    # Given
    project = make_experiment_project(id=1)
    repository_mock.get_project_by_id.return_value = project
    project_service.repository = repository_mock

    project_dto = PatchProjectRequestDTO(
        experiment_type=ExperimentTypeEnum.OFFLINE,
        location="Change location",
    )
    # When
    await project_service.update_project(
        workspace_id=1,
        project_id=1,
        project_type=ProjectTypeEnum.EXPERIMENT,
        project_dto=project_dto,
    )


@pytest.mark.asyncio
async def test_delete_project_not_exist():
    # Given
    repository_mock.get_project_by_id.return_value = None
    project_service.repository = repository_mock

    # When, Then
    with pytest.raises(ProjectNotFoundException):
        await project_service.delete_project(
            workspace_id=1,
            project_id=2,
            project_type=ProjectTypeEnum.EXPERIMENT,
        )


@pytest.mark.asyncio
async def test_delete_project_access_denied():
    # Given
    project = make_experiment_project(id=1)
    repository_mock.get_project_by_id.return_value = project
    project_service.repository = repository_mock

    # When, Then
    with pytest.raises(ProjectAccessDeniedException):
        await project_service.delete_project(
            workspace_id=2,
            project_id=2,
            project_type=ProjectTypeEnum.EXPERIMENT,
        )


@pytest.mark.asyncio
async def test_delete_project():
    # Given
    project = make_experiment_project(id=1)
    repository_mock.get_project_by_id.return_value = project
    project_service.repository = repository_mock

    # When, Then
    await project_service.delete_project(
        workspace_id=1,
        project_id=project.id,
        project_type=ProjectTypeEnum.EXPERIMENT,
    )


@pytest.mark.asyncio
async def test_get_project_participant_list():
    # Given
    experiment_participant_time_slot = ExperimentParticipantTimeSlotRead(
        id=1,
        username="username",
        reserved_date="2024-04-09 10:00AM ~ 11:00AM",
        attendance_status=ExperimentAttendanceStatus.ATTENDED.value,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    repository_mock.get_project_participants.return_value = [
        experiment_participant_time_slot
    ]
    project_service.repository = repository_mock

    # When
    sut = await project_service.get_project_participant_list(
        workspace_id=1,
        project_id=1,
        project_type=ProjectTypeEnum.EXPERIMENT,
        page=1,
        size=12,
    )
    # Then
    assert len(sut) == 1
    result = sut[0]
    assert result.id == experiment_participant_time_slot.id
    assert (
        result.attendance_status == experiment_participant_time_slot.attendance_status
    )


@pytest.mark.asyncio
async def test_delete_project_participant():
    # Given
    project_participant = make_experiment_project_participant(id=1)
    repository_mock.get_project_participant_by_id.return_value = project_participant
    project_service.repository = repository_mock

    # When, Then
    await project_service.delete_project_participant(
        workspace_id=1,
        project_id=1,
        participant_id=project_participant.id,
        project_type=ProjectTypeEnum.EXPERIMENT,
    )
