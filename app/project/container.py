from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.project.adapter.output.persistence.repository_adapter import (
    ProjectRepositoryAdapter,
)
from app.project.adapter.output.persistence.sqlalchemy.project import (
    ProjectSQLAlchemyRepo,
)
from app.project.application.service.project import ProjectService


class ProjectContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=["app"])

    project_sqlalchemy_repo = Singleton(ProjectSQLAlchemyRepo)
    project_repository_adapter = Factory(
        ProjectRepositoryAdapter,
        repository=project_sqlalchemy_repo,
    )
    project_service = Factory(ProjectService, repository=project_repository_adapter)
