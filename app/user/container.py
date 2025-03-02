from dependency_injector import containers, providers

from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.user.application.service.user import UserService
from core.helpers.cache.base.backend import BaseBackend


class UserContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.auth.adapter.input.api.v1.auth",
            "app.user.adapter.input.api.v1.user",
        ]
    )

    user_sqlalchemy_repo = providers.Singleton(UserSQLAlchemyRepo)
    user_repository_adapter = providers.Factory(
        UserRepositoryAdapter,
        repository=user_sqlalchemy_repo,
    )

    redis_backend: providers.Provider[BaseBackend] = providers.Dependency()

    user_service = providers.Factory(
        UserService,
        repository=user_repository_adapter,
        cache=redis_backend,
    )
