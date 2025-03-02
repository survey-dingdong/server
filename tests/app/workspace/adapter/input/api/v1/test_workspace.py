import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.server import app
from app.workspace.application.exception import (
    TooManyWorkspacesException,
    WorkspaceAccessDeniedException,
    WorkspaceNotFoundeException,
    WrongOrderNoWorkspacesException,
)
from tests.support.user_fixture import make_user
from tests.support.workspace_fixture import make_workspace

BASE_URL = "http://test"


@pytest.mark.asyncio
async def test_get_workspaces(session: AsyncSession, access_token: str) -> None:
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )
    session.add(user)

    workspace = make_workspace(id=1)
    session.add(workspace)
    await session.commit()

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/workspaces",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    # Then
    sut = response.json()
    assert len(sut) == 1
    assert sut[0] == {"id": 1, "title": "workspace", "order_no": 1}


@pytest.mark.asyncio
async def test_create_workspace_too_many(
    session: AsyncSession, access_token: str
) -> None:
    # Given
    user = make_user(
        id=1,
        password="password",
        email="a@b.c",
        username="dingdong-survey",
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
        response = await client.post(
            "/workspaces",
            headers={"Authorization": f"Bearer {access_token}"},
            json=body,
        )

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_create_workspace(session: AsyncSession, access_token: str) -> None:
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )
    session.add(user)
    await session.commit()

    body = {
        "title": "workspace",
    }

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/workspaces",
            headers={"Authorization": f"Bearer {access_token}"},
            json=body,
        )

    # Then
    sut = response.json()
    assert sut["id"] == 1


@pytest.mark.asyncio
async def test_update_workspace_not_exist(
    session: AsyncSession, access_token: str
) -> None:
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )
    session.add(user)

    workspace = make_workspace(id=1)
    session.add(workspace)
    await session.commit()

    exc = WorkspaceNotFoundeException
    body = {
        "title": "workspace",
    }

    # When
    invalid_workspace_id = 2
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.patch(
            f"/workspaces/{invalid_workspace_id}",
            headers={"Authorization": f"Bearer {access_token}"},
            json=body,
        )

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_update_workspace_access_denied(
    session: AsyncSession, access_token: str
) -> None:
    # Given
    user1 = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )
    user2 = make_user(
        id=2,
        password="password",
        email="a2@b.c",
        username="dingdong-survey2",
        is_admin=True,
    )
    session.add_all([user1, user2])

    workspace1 = make_workspace(id=1)
    workspace2 = make_workspace(id=2, user_id=2)
    session.add_all([workspace1, workspace2])
    await session.commit()

    exc = WorkspaceAccessDeniedException
    body = {
        "title": "workspace2",
    }

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.patch(
            f"/workspaces/{workspace2.id}",
            headers={"Authorization": f"Bearer {access_token}"},
            json=body,
        )

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_update_workspace_wrong_order_no(
    session: AsyncSession, access_token: str
) -> None:
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )
    session.add(user)

    workspace = make_workspace(id=1)
    session.add(workspace)
    await session.commit()

    exc = WrongOrderNoWorkspacesException
    body = {
        "order_no": 2,
    }

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.patch(
            f"/workspaces/{workspace.id}",
            headers={"Authorization": f"Bearer {access_token}"},
            json=body,
        )

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_update_workspace(session: AsyncSession, access_token: str) -> None:
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )
    session.add(user)

    workspace = make_workspace(id=1)
    session.add(workspace)
    await session.commit()

    body = {
        "title": "workspace2",
    }

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.patch(
            f"/workspaces/{workspace.id}",
            headers={"Authorization": f"Bearer {access_token}"},
            json=body,
        )

    # Then
    sut = response.json()
    assert sut is None


@pytest.mark.asyncio
async def test_delete_workspace_not_exist(
    session: AsyncSession, access_token: str
) -> None:
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )
    session.add(user)

    workspace = make_workspace(id=1)
    session.add(workspace)
    await session.commit()

    exc = WorkspaceNotFoundeException

    # When
    invalid_workspace_id = 2
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete(
            f"/workspaces/{invalid_workspace_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_delete_workspace_access_denied(
    session: AsyncSession, access_token: str
) -> None:
    # Given
    user = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )
    session.add(user)

    workspace = make_workspace(id=1)
    session.add(workspace)
    await session.commit()

    exc = WorkspaceNotFoundeException

    # When
    invalid_workspace_id = 2
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete(
            f"/workspaces/{invalid_workspace_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }


@pytest.mark.asyncio
async def test_delete_workspace(session: AsyncSession, access_token: str) -> None:
    # Given
    user1 = make_user(
        password="password",
        email="a@b.c",
        username="dingdong-survey",
        is_admin=True,
    )
    user2 = make_user(
        id=2,
        password="password",
        email="a2@b.c",
        username="dingdong-survey2",
        is_admin=True,
    )
    session.add_all([user1, user2])

    workspace1 = make_workspace(id=1)
    workspace2 = make_workspace(id=2, user_id=2)
    session.add_all([workspace1, workspace2])
    await session.commit()

    exc = WorkspaceAccessDeniedException

    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete(
            f"/workspaces/{workspace2.id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    # Then
    assert response.json() == {
        "error_code": exc.error_code,
        "message": exc.message,
    }
