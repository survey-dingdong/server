from sqlalchemy import and_, func, select, update

from app.workspace.domain.entity.workspace import Workspace
from app.workspace.domain.repository.workspace import WorkspaceRepo
from core.db.session import session


class WorkspaceSQLAlchemyRepo(WorkspaceRepo):
    async def get_workspaces(
        self, user_id: int, page: int, size: int
    ) -> list[Workspace]:
        query = (
            select(Workspace)
            .where(
                and_(
                    Workspace.user_id == user_id,
                    Workspace.is_deleted == False,  # noqa: E712
                )
            )
            .order_by(Workspace.order)
        )

        query = query.offset((page - 1) * size).limit(size)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_workspace_by_id(self, workspace_id: int) -> Workspace | None:
        query = select(Workspace).where(
            and_(
                Workspace.id == workspace_id,
                Workspace.is_deleted == False,  # noqa: E712
            )
        )
        result = await session.execute(query)
        return result.scalars().first()

    async def reorder_workspace(self, order: int) -> None:
        query = (
            update(Workspace)
            .where(Workspace.order >= order)
            .values(order=Workspace.order + 1)
        )
        await session.execute(query)

    async def count(self, user_id: int) -> int:
        query = (
            select(func.count())
            .select_from(Workspace)
            .where(Workspace.user_id == user_id)
        )
        obj_count: int = await session.scalar(query)
        return obj_count

    async def save(self, workspace: Workspace, auto_flush: bool = False) -> Workspace:
        session.add(workspace)
        if auto_flush:
            await session.flush()
        return workspace
