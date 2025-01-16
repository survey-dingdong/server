from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.websocket.application.service.websocket import WebsocketService
from core.helpers.cache.socket_manager import WebSocketManager


class WebsocketContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=[".adapter.input.api.v1.websocket"])

    websocket_manager = Singleton(WebSocketManager)
    websocket_service = Factory(WebsocketService, websocket_manager=websocket_manager)
