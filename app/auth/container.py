from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.auth.adapter.output.external_system.email.auth import EmailSender
from app.auth.adapter.output.external_system.external_system_adapter import (
    ExternalSystemAdapter,
)
from app.auth.application.service.auth import AuthService


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["app.auth.adapter.input.api.v1.auth"])

    auth_email_sender = Singleton(EmailSender)
    auth_external_system_adapter = Factory(
        ExternalSystemAdapter,
        port=auth_email_sender,
    )
    auth_service = Factory(AuthService, port=auth_external_system_adapter)
