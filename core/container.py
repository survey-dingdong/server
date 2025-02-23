from dependency_injector import containers, providers

from app.auth.container import AuthContainer
from app.project.container import ProjectContainer
from app.user.container import UserContainer
from app.workspace.container import WorkspaceContainer
from core.helpers.cache.redis_backend import RedisBackend


class CoreContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["core.fastapi.middlewares.authentication"]
    )

    redis_backend = providers.Singleton(RedisBackend)


class AppContainer(containers.DeclarativeContainer):
    core = providers.Container(CoreContainer)

    auth = providers.Container(AuthContainer, redis_backend=core.redis_backend)

    user = providers.Container(UserContainer, redis_backend=core.redis_backend)

    project = providers.Container(ProjectContainer)

    workspace = providers.Container(WorkspaceContainer)
