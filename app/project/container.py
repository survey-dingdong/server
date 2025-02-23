from dependency_injector import containers, providers

from app.project.adapter.output.persistence.repository_adapter import (
    ProjectRepositoryAdapter,
)
from app.project.adapter.output.persistence.sqlalchemy.project import (
    ProjectSQLAlchemyRepo,
)
from app.project.application.service.project import ProjectService


class ProjectContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.project.adapter.input.api.v1.project",
        ]
    )

    project_sqlalchemy_repo = providers.Singleton(ProjectSQLAlchemyRepo)
    project_repository_adapter = providers.Factory(
        ProjectRepositoryAdapter,
        repository=project_sqlalchemy_repo,
    )
    project_service = providers.Factory(
        ProjectService, repository=project_repository_adapter
    )
