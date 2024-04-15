from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.workspace.adapter.output.persistence.repository_adapter import (
    WorkspaceRepositoryAdapter,
)
from app.workspace.adapter.output.persistence.sqlalchemy.workspace import (
    WorkspaceSQLAlchemyRepo,
)
from app.workspace.application.service.workspace import WorkspaceService


class WorkspaceContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=["app"])

    workspace_sqlalchemy_repo = Singleton(WorkspaceSQLAlchemyRepo)
    workspace_repository_adapter = Factory(
        WorkspaceRepositoryAdapter,
        repository=workspace_sqlalchemy_repo,
    )
    workspace_service = Factory(
        WorkspaceService, repository=workspace_repository_adapter
    )
