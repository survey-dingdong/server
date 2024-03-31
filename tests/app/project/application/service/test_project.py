from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.project.adapter.output.persistence.repository_adapter import (
    ProjectRepositoryAdapter,
)
from app.project.application.service.project import ProjectService
from app.project.domain.command import CreateProjectCommand
from app.project.domain.entity.project import ProjectRead
from app.project.domain.vo.type import ProjectTypeEnum
from tests.support.project_fixture import make_project

repository_mock = AsyncMock(spec=ProjectRepositoryAdapter)
project_service = ProjectService(repository=repository_mock)


@pytest.mark.asyncio
async def test_get_project_list():
    # Given
    project = ProjectRead(
        id=1,
        workspace_id=1,
        title="project",
        project_type=ProjectTypeEnum.EXPERIMENT,
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
        workspace_id=1, filter_project_type=ProjectTypeEnum.EXPERIMENT
    )

    # Then
    assert len(sut) == 1
    result = sut[0]
    assert result.id == project.id
    assert result.workspace_id == project.workspace_id
    assert result.title == project.title
    assert result.project_type == project.project_type


@pytest.mark.asyncio
async def test_get_project_by_id():
    # Given
    project = make_project(id=1)
    repository_mock.get_project_by_id.return_value = project
    project_service.repository = repository_mock

    # When
    sut = await project_service.get_project(
        workspace_id=1,
        project_id=project.id,
        filter_project_type=ProjectTypeEnum.EXPERIMENT,
    )
    assert sut.id == 1


@pytest.mark.asyncio
async def test_create_project():
    # Given
    command = CreateProjectCommand(
        workspace_id=1, title="project", project_type=ProjectTypeEnum.EXPERIMENT
    )

    # When
    sut = await project_service.create_project(command=command)

    # Then
    assert sut.id == 1
