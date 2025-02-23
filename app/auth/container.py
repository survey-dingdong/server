from dependency_injector import containers, providers

from app.auth.adapter.output.external_system.email.auth import EmailSender
from app.auth.adapter.output.external_system.external_system_adapter import (
    ExternalSystemAdapter,
)
from app.auth.application.service.auth import AuthService
from core.helpers.cache.base.backend import BaseBackend


class AuthContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["app.auth.adapter.input.api.v1.auth"]
    )

    auth_email_sender = providers.Singleton(EmailSender)
    auth_external_system_adapter = providers.Factory(
        ExternalSystemAdapter,
        port=auth_email_sender,
    )

    redis_backend: providers.Provider[BaseBackend] = providers.Dependency()

    auth_service = providers.Factory(
        AuthService,
        port=auth_external_system_adapter,
        cache=redis_backend,
    )
