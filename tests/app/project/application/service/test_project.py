from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.project.adapter.output.persistence.repository_adapter import (
    ProjectRepositoryAdapter,
)
from app.project.application.dto import UpdateProjectRequestDTO
from app.project.application.exception import (
    ProjectAccessDeniedException,
    ProjectNotFoundException,
)
from app.project.application.service.project import ProjectService
from app.project.domain.command import CreateProjectCommand
from app.project.domain.entity.experiment import ExperimentParticipantTimeslotRead
from app.project.domain.entity.project import ProjectRead
from app.project.domain.vo import (
    ExperimentAttendanceStatusTypeEnum,
    ExperimentTypeEnum,
    ProjectTypeEnum,
)
from tests.support.project_fixture import (
    make_experiment_project,
    make_experiment_project_participant,
)
from tests.support.workspace_fixture import make_workspace

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
        filter_title="project",
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

    # When, Then
    with pytest.raises(ProjectNotFoundException):
        await project_service.get_project(
            user_id=1,
            project_id=2,
            project_type=ProjectTypeEnum.EXPERIMENT,
        )


@pytest.mark.asyncio
async def test_get_project_by_id():
    # Given
    workspace = make_workspace(id=1)
    project = make_experiment_project(id=1)
    project.workspace = workspace

    repository_mock.get_project_by_id.return_value = project
    project_service.repository = repository_mock

    # When
    sut = await project_service.get_project(
        user_id=1,
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

    project_dto = UpdateProjectRequestDTO(
        title="Change title",
        description="",
        is_public=False,
        start_date=datetime.now().date().strftime("%Y-%m-%d"),
        end_date=datetime.now().date().strftime("%Y-%m-%d"),
        excluded_dates=[],
        experiment_timeslots=[],
        max_participants=0,
        experiment_type=ExperimentTypeEnum.OFFLINE,
        location="Change location",
    )

    # When, Then
    with pytest.raises(ProjectNotFoundException):
        await project_service.update_project(
            user_id=1,
            project_id=2,
            project_type=ProjectTypeEnum.EXPERIMENT,
            project_dto=project_dto,
        )


@pytest.mark.asyncio
async def test_updated_project():
    # Given
    workspace = make_workspace(id=1)
    project = make_experiment_project(id=1)
    project.workspace = workspace

    repository_mock.get_project_by_id.return_value = project
    project_service.repository = repository_mock

    project_dto = UpdateProjectRequestDTO(
        title="change title",
        description=project.description,
        is_public=project.is_public,
        start_date=project.start_date,
        end_date=project.end_date,
        excluded_dates=project.excluded_dates,
        experiment_timeslots=project.experiment_timeslots,
        max_participants=project.max_participants,
        experiment_type=project.experiment_type,
        location="Change location",
    )
    # When
    await project_service.update_project(
        user_id=1,
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
            user_id=1,
            project_id=2,
            project_type=ProjectTypeEnum.EXPERIMENT,
        )


@pytest.mark.asyncio
async def test_delete_project():
    # Given
    workspace = make_workspace(id=1)
    project = make_experiment_project(id=1)
    project.workspace = workspace

    repository_mock.get_project_by_id.return_value = project
    project_service.repository = repository_mock

    # When, Then
    await project_service.delete_project(
        user_id=1,
        project_id=project.id,
        project_type=ProjectTypeEnum.EXPERIMENT,
    )


@pytest.mark.asyncio
async def test_get_project_participant_list():
    # Given
    experiment_participant_timeslot = ExperimentParticipantTimeslotRead(
        id=1,
        username="username",
        experiment_date="2024-04-09",
        start_time="10:00",
        end_time="11:00",
        attendance_status=ExperimentAttendanceStatusTypeEnum.ATTENDED.value,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    repository_mock.get_project_participants.return_value = [
        experiment_participant_timeslot
    ]
    project_service.repository = repository_mock

    # When
    sut = await project_service.get_project_participant_list(
        user_id=1,
        project_id=1,
        project_type=ProjectTypeEnum.EXPERIMENT,
        page=1,
        size=12,
    )
    # Then
    assert len(sut) == 1
    result = sut[0]
    assert result.id == experiment_participant_timeslot.id
    assert result.attendance_status == experiment_participant_timeslot.attendance_status


@pytest.mark.asyncio
async def test_update_project_participant_access_denied():
    # Given
    workspace = make_workspace(id=1)
    project = make_experiment_project(id=1)
    project.workspace = workspace
    repository_mock.get_project_by_id.return_value = project

    project_participant = make_experiment_project_participant(id=1)
    repository_mock.get_project_participant_by_id.return_value = project_participant

    project_service.repository = repository_mock

    # When, Then
    with pytest.raises(ProjectAccessDeniedException):
        await project_service.update_project_participant_status(
            user_id=2,
            project_id=1,
            participant_id=project_participant.id,
            project_type=ProjectTypeEnum.EXPERIMENT,
            attendance_status=ExperimentAttendanceStatusTypeEnum.NOT_ATTENDED,
        )


@pytest.mark.asyncio
async def test_update_project_participant():
    # Given
    workspace = make_workspace(id=1)
    project = make_experiment_project(id=1)
    project.workspace = workspace
    repository_mock.get_project_by_id.return_value = project

    project_participant = make_experiment_project_participant(id=1)
    repository_mock.get_project_participant_by_id.return_value = project_participant

    project_service.repository = repository_mock

    # When, Then
    await project_service.update_project_participant_status(
        user_id=1,
        project_id=1,
        participant_id=project_participant.id,
        project_type=ProjectTypeEnum.EXPERIMENT,
        attendance_status=ExperimentAttendanceStatusTypeEnum.NOT_ATTENDED,
    )


@pytest.mark.asyncio
async def test_delete_project_participant_access_denied():
    # Given
    project_participant = make_experiment_project_participant(id=1)
    repository_mock.get_project_participant_by_id.return_value = project_participant
    project_service.repository = repository_mock

    # When, Then
    with pytest.raises(ProjectAccessDeniedException):
        await project_service.delete_project_participant(
            user_id=2,
            project_id=1,
            participant_id=project_participant.id,
            project_type=ProjectTypeEnum.EXPERIMENT,
        )


@pytest.mark.asyncio
async def test_delete_project_participant():
    # Given
    project_participant = make_experiment_project_participant(id=1)
    repository_mock.get_project_participant_by_id.return_value = project_participant
    project_service.repository = repository_mock

    # When, Then
    await project_service.delete_project_participant(
        user_id=1,
        project_id=1,
        participant_id=project_participant.id,
        project_type=ProjectTypeEnum.EXPERIMENT,
    )
