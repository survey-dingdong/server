from abc import ABC, abstractmethod

from fastapi import WebSocket


class ChatUseCase(ABC):
    @abstractmethod
    async def send_chat(self, websocket: WebSocket, room_id: str, user_id: int) -> None:
        """Send chat"""
