from sqlalchemy import func, select

from app.workspace.domain.entity.workspace import Workspace
from app.workspace.domain.repository.workspace import WorkspaceRepo
from core.db.session import session


class WorkspaceSQLAlchemyRepo(WorkspaceRepo):
    async def get_workspaces(
        self,
        user_id: int,
    ) -> list[Workspace]:
        query = select(Workspace).where(Workspace.user_id == user_id)
        result = await session.execute(query)
        return result.scalars().all()

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
