from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.user.application.service.user import UserService
from core.helpers.cache.redis_backend import RedisBackend


class UserContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=[".adapter.input.api.v1.user"])

    user_sqlalchemy_repo = Singleton(UserSQLAlchemyRepo)
    user_repository_adapter = Factory(
        UserRepositoryAdapter,
        repository=user_sqlalchemy_repo,
    )
    redis_backend = Singleton(RedisBackend)
    user_service = Factory(
        UserService, repository=user_repository_adapter, cache=redis_backend
    )
