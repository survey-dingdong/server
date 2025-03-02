from dependency_injector import containers, providers

from app.workspace.adapter.output.persistence.repository_adapter import (
    WorkspaceRepositoryAdapter,
)
from app.workspace.adapter.output.persistence.sqlalchemy.workspace import (
    WorkspaceSQLAlchemyRepo,
)
from app.workspace.application.service.workspace import WorkspaceService


class WorkspaceContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.workspace.adapter.input.api.v1.workspace",
            "app.project.adapter.input.api.v1.project",
        ]
    )

    workspace_sqlalchemy_repo = providers.Singleton(WorkspaceSQLAlchemyRepo)
    workspace_repository_adapter = providers.Factory(
        WorkspaceRepositoryAdapter,
        repository=workspace_sqlalchemy_repo,
    )
    workspace_service = providers.Factory(
        WorkspaceService, repository=workspace_repository_adapter
    )
