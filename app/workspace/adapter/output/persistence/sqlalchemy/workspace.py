from sqlalchemy import select

from app.workspace.domain.entity.workspace import Workspace
from app.workspace.domain.repository.workspace import WorkspaceRepo
from core.db.session import session


class WorkspaceSQLAlchemyRepo(WorkspaceRepo):
    async def get_workspaces(
        self,
    ) -> list[Workspace]:
        query = select(Workspace)
        result = await session.execute(query)
        return result.scalars().all()

    async def save(self, *, workspace: Workspace) -> None:
        session.add(workspace)
