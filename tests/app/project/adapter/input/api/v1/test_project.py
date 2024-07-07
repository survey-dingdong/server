import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.project.application.exception import ProjectNotFoundException
from app.server import app
from tests.support.constants import USER_ID_1_TOKEN
from tests.support.project_fixture import make_experiment_project
from tests.support.user_fixture import make_user
from tests.support.workspace_fixture import make_workspace

HEADERS = {"Authorization": f"Bearer {USER_ID_1_TOKEN}"}
BASE_URL = "http://test"


@pytest.mark.asyncio
async def test_get_project_list(session: AsyncSession):
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

    params = {"project_type": "experiment"}
    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            f"/workspaces/{workspace.id}/projects", headers=HEADERS, params=params
        )

    # Then
    sut = response.json()
    assert len(sut) == 1
    assert sut[0] == {
        "id": 1,
        "workspace_id": 1,
        "title": "project",
        "description": "",
        "is_public": False,
        "joined_participants": 0,
        "max_participants": 0,
        "created_at": experiment_project.created_at,
        "updated_at": experiment_project.updated_at,
    }


@pytest.mark.asyncio
async def test_get_project_not_exist(session: AsyncSession):
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
    params = {"project_type": "experiment"}

    # When
    invalid_experiment_project_id = 2
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            f"/projects/{invalid_experiment_project_id}",
            headers=HEADERS,
            params=params,
        )

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_get_project_by_id(session: AsyncSession):
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

    params = {"project_type": "experiment"}

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            f"/projects/{experiment_project.id}",
            headers=HEADERS,
            params=params,
        )

    # Then
    sut = response.json()
    assert sut == {
        "id": 1,
        "title": "project",
        "description": "",
        "is_public": False,
        "start_date": experiment_project.start_date,
        "end_date": experiment_project.end_date,
        "excluded_dates": experiment_project.excluded_dates,
        "experiment_timeslots": [],
        "max_participants": 0,
        "experiment_type": experiment_project.experiment_type.value,
        "location": experiment_project.location,
        "created_at": experiment_project.created_at,
        "updated_at": experiment_project.updated_at,
    }


@pytest.mark.asyncio
async def test_create_project(session: AsyncSession):
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

    params = {"project_type": "experiment"}
    body = {
        "title": "project",
    }

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            f"/workspaces/{workspace.id}/projects",
            headers=HEADERS,
            json=body,
            params=params,
        )

    # Then
    sut = response.json()
    assert sut["id"] == 1


@pytest.mark.asyncio
async def test_update_project_not_exist(session: AsyncSession):
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
    params = {"project_type": "experiment"}
    body = {
        "title": "Change title",
        "description": "detial",
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
            params=params,
        )

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_update_project(session: AsyncSession):
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

    params = {"project_type": "experiment"}
    body = {
        "title": "Change title",
        "description": "detial",
        "is_public": True,
        "start_date": "2024-05-05",
        "end_date": "2024-05-12",
        "excluded_dates": ["2024-05-10"],
        "experiment_timeslots": [
            {
                "start_time": "10:00",
                "end_time": "10:30",
                "max_participants": 0,
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
            params=params,
        )

    # Then
    sut = response.json()
    assert sut is None


@pytest.mark.asyncio
async def test_delete_project_not_exist(session: AsyncSession):
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
    params = {"project_type": "experiment"}

    # When
    invalid_experiment_project_id = 1
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete(
            f"/projects/{invalid_experiment_project_id}",
            headers=HEADERS,
            params=params,
        )

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_delete_project(session: AsyncSession):
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

    params = {"project_type": "experiment"}

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete(
            f"/projects/{experiment_project.id}",
            headers=HEADERS,
            params=params,
        )

    # Then
    sut = response.json()
    assert sut is None
