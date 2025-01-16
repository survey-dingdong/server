import json

from fastapi import WebSocket, WebSocketDisconnect

from app.chat.domain.usecase.chat import ChatUseCase
from core.helpers.cache.socket_manager import WebSocketManager


class ChatService(ChatUseCase):
    def __init__(self, websocket_manager: WebSocketManager) -> None:
        self.websocket_manager = websocket_manager

    async def send_chat(self, websocket: WebSocket, room_id: str, user_id: int) -> None:
        await self.websocket_manager.add_user_to_room(room_id, websocket)
        message = {
            "user_id": user_id,
            "room_id": room_id,
            "message": f"User {user_id} connected to room - {room_id}",
        }
        await self.websocket_manager.broadcast_to_room(room_id, json.dumps(message))
        try:
            while True:
                data = await websocket.receive_text()
                message = {"user_id": user_id, "room_id": room_id, "message": data}
                await self.websocket_manager.broadcast_to_room(
                    room_id, json.dumps(message)
                )

        except WebSocketDisconnect:
            await self.websocket_manager.remove_user_from_room(room_id, websocket)

            message = {
                "user_id": user_id,
                "room_id": room_id,
                "message": f"User {user_id} disconnected from room - {room_id}",
            }
            await self.websocket_manager.broadcast_to_room(room_id, json.dumps(message))
