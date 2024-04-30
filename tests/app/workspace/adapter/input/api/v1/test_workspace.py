import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.server import app
from app.workspace.application.exception import TooManyWorkspacesException
from tests.support.constants import USER_ID_1_TOKEN
from tests.support.user_fixture import make_user
from tests.support.workspace_fixture import make_workspace

HEADERS = {"Authorization": f"Bearer {USER_ID_1_TOKEN}"}
BASE_URL = "http://test"


@pytest.mark.asyncio
async def test_get_workspaces(session: AsyncSession):
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        nickname="survey-dingdong",
        is_admin=True,
    )
    session.add(user)

    workspace = make_workspace(id=1)
    session.add(workspace)
    await session.commit()

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/workspaces", headers=HEADERS)

    # Then
    sut = response.json()
    assert len(sut) == 1
    assert sut[0] == {"id": 1, "title": "workspace", "order_no": 1}


@pytest.mark.asyncio
async def test_create_workspace_too_many(session: AsyncSession):
    # Given
    user = make_user(
        id=1,
        password="password",
        email="a@b.c",
        nickname="survey-dingdong",
        is_admin=True,
    )
    session.add(user)

    workspaces = [
        make_workspace(
            id=i,
            user_id=user.id,
            title=f"workspace{i}",
            order_no=i,
        )
        for i in range(1, 11)
    ]
    session.add_all(workspaces)
    await session.commit()

    exc = TooManyWorkspacesException
    body = {
        "title": "workspace123",
    }
    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/workspaces", headers=HEADERS, json=body)

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_create_workspace(session: AsyncSession):
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        nickname="survey-dingdong",
        is_admin=True,
    )
    session.add(user)
    await session.commit()

    body = {
        "title": "workspace",
    }

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/workspaces", headers=HEADERS, json=body)

    # Then
    sut = response.json()
    assert sut["id"] == 1
