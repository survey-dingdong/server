import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.project.application.exception import ProjectNotFoundException
from app.server import app
from tests.support.constants import USER_ID_1_TOKEN
from tests.support.project_fixture import (
    make_experiment_project,
    make_experiment_timeslot,
)
from tests.support.user_fixture import make_user
from tests.support.workspace_fixture import make_workspace

HEADERS = {"Authorization": f"Bearer {USER_ID_1_TOKEN}"}
BASE_URL = "http://test"


@pytest.mark.asyncio
async def test_get_project_list(session: AsyncSession) -> None:
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )

    workspace = make_workspace(id=1)

    experiment_project = make_experiment_project(id=1, workspace_id=workspace.id)

    session.add_all([user, workspace, experiment_project])
    await session.commit()

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            f"/workspaces/{workspace.id}/projects", headers=HEADERS
        )

    # Then
    sut = response.json()
    assert len(sut) == 1

    assert sut[0]["id"] == experiment_project.id
    assert sut[0]["workspace_id"] == experiment_project.workspace_id
    assert sut[0]["title"] == experiment_project.title
    assert sut[0]["description"] == experiment_project.description
    assert sut[0]["is_public"] == experiment_project.is_public
    assert sut[0]["joined_participants"] == experiment_project.joined_participants
    assert sut[0]["max_participants"] == experiment_project.max_participants


@pytest.mark.asyncio
async def test_get_project_not_exist(session: AsyncSession) -> None:
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )

    workspace = make_workspace(id=1)

    experiment_project = make_experiment_project(id=1, workspace_id=workspace.id)

    session.add_all([user, workspace, experiment_project])
    await session.commit()

    exc = ProjectNotFoundException

    # When
    invalid_experiment_project_id = 2
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            f"/projects/{invalid_experiment_project_id}",
            headers=HEADERS,
        )

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_get_project_by_id(session: AsyncSession) -> None:
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )

    workspace = make_workspace(id=1)

    experiment_project = make_experiment_project(id=1, workspace_id=workspace.id)

    session.add_all([user, workspace, experiment_project])
    await session.commit()

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            f"/projects/{experiment_project.id}",
            headers=HEADERS,
        )

    # Then
    sut = response.json()
    assert sut["id"] == experiment_project.id
    assert sut["title"] == experiment_project.title
    assert sut["description"] == experiment_project.description
    assert sut["is_public"] == experiment_project.is_public
    assert sut["start_date"] == experiment_project.start_date
    assert sut["end_date"] == experiment_project.end_date
    assert sut["excluded_dates"] == experiment_project.excluded_dates
    assert sut["experiment_timeslots"] == []
    assert sut["max_participants"] == experiment_project.max_participants
    assert sut["experiment_type"] == experiment_project.experiment_type.value
    assert sut["location"] == experiment_project.location


@pytest.mark.asyncio
async def test_create_project(session: AsyncSession) -> None:
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )

    workspace = make_workspace(id=1)
    session.add_all([user, workspace])
    await session.commit()

    body = {
        "title": "project",
    }

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/workspaces/{workspace.id}/projects",
            headers=HEADERS,
            json=body,
        )

    # Then
    sut = response.json()
    assert sut["id"] == 1


@pytest.mark.asyncio
async def test_update_project_not_exist(session: AsyncSession) -> None:
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )

    workspace = make_workspace(id=1)

    experiment_project = make_experiment_project(id=1, workspace_id=workspace.id)

    session.add_all([user, workspace, experiment_project])
    await session.commit()

    exc = ProjectNotFoundException
    body = {
        "title": "Change title",
        "description": "detail",
        "is_public": True,
        "start_date": "2024-05-05",
        "end_date": "2024-05-12",
        "excluded_dates": ["2024-05-10"],
        "experiment_timeslots": [
            {
                "id": 1,
                "start_time": "10:00",
                "end_time": "10:30",
                "max_participants": 0,
            }
        ],
        "max_participants": 0,
        "experiment_type": "online",
        "location": "string",
    }

    # When
    invalid_experiment_project_id = 2
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put(
            f"/projects/{invalid_experiment_project_id}",
            headers=HEADERS,
            json=body,
        )

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_update_project(session: AsyncSession) -> None:
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )

    workspace = make_workspace(id=1)

    experiment_project = make_experiment_project(id=1, workspace_id=workspace.id)

    experiment_timeslot = make_experiment_timeslot(
        id=1, experiment_project_id=experiment_project.id
    )

    session.add_all([user, workspace, experiment_project, experiment_timeslot])
    await session.commit()

    body = {
        "title": "Change title",
        "description": "detail",
        "is_public": True,
        "start_date": "2024-05-05",
        "end_date": "2024-05-12",
        "excluded_dates": ["2024-05-10"],
        "experiment_timeslots": [
            {
                "id": experiment_timeslot.id,
                "start_time": "10:00",
                "end_time": "10:30",
                "max_participants": 5,
            },
            {
                "start_time": "11:00",
                "end_time": "11:30",
                "max_participants": 2,
            },
        ],
        "max_participants": 2,
        "experiment_type": "online",
        "location": "string",
    }

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put(
            f"/projects/{experiment_project.id}",
            headers=HEADERS,
            json=body,
        )

    # Then
    sut = response.json()
    assert sut is None


@pytest.mark.asyncio
async def test_delete_project_not_exist(session: AsyncSession) -> None:
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )

    workspace = make_workspace(id=1)

    session.add_all([user, workspace])
    await session.commit()

    exc = ProjectNotFoundException

    # When
    invalid_experiment_project_id = 1
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete(
            f"/projects/{invalid_experiment_project_id}",
            headers=HEADERS,
        )

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_delete_project(session: AsyncSession) -> None:
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )

    workspace = make_workspace(id=1)

    experiment_project = make_experiment_project(id=1, workspace_id=workspace.id)

    session.add_all([user, workspace, experiment_project])
    await session.commit()

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete(
            f"/projects/{experiment_project.id}",
            headers=HEADERS,
        )

    # Then
    sut = response.json()
    assert sut is None
