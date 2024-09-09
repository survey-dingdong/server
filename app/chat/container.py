from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.chat.application.service.chat import ChatService
from core.helpers.cache.socket_manager import WebSocketManager


class ChatContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(modules=[".adapter.input.api.v1.chat"])

    websocket_manager = Singleton(WebSocketManager)
    chat_service = Factory(ChatService, websocket_manager=websocket_manager)
