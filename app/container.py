from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory

from app.auth.application.service.jwt import JwtService


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["app"])

    jwt_service = Factory(JwtService)
