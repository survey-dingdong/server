import asyncio

from fastapi import WebSocket
from redis.asyncio.client import PubSub

from core.helpers.redis import redis_client


class RedisPubSubManager:
    def __init__(self):
        self.pubsub = None

    async def connect(self) -> None:
        self.pubsub = redis_client.pubsub()

    async def _publish(self, room_id: str, message: str) -> None:
        await redis_client.publish(room_id, message)

    async def subscribe(self, room_id: str) -> PubSub:
        await self.pubsub.subscribe(room_id)
        return self.pubsub

    async def unsubscribe(self, room_id: str) -> None:
        await self.pubsub.unsubscribe(room_id)


class WebSocketManager:
    def __init__(self):
        self.rooms: dict = {}
        self.pubsub_client = RedisPubSubManager()

    async def add_user_to_room(self, room_id: str, websocket: WebSocket) -> None:
        await websocket.accept()

        if room_id in self.rooms:
            self.rooms[room_id].append(websocket)
        else:
            self.rooms[room_id] = [websocket]

            await self.pubsub_client.connect()
            pubsub_subscriber: PubSub = await self.pubsub_client.subscribe(room_id)
            asyncio.create_task(self._pubsub_data_reader(pubsub_subscriber))

    async def broadcast_to_room(self, room_id: str, message: str) -> None:
        await self.pubsub_client._publish(room_id, message)

    async def remove_user_from_room(self, room_id: str, websocket: WebSocket) -> None:
        self.rooms[room_id].remove(websocket)

        if len(self.rooms[room_id]) == 0:
            del self.rooms[room_id]
            await self.pubsub_client.unsubscribe(room_id)

    async def _pubsub_data_reader(self, pubsub_subscriber: PubSub):
        while True:
            message = await pubsub_subscriber.get_message(
                ignore_subscribe_messages=True
            )
            if message is not None:
                room_id = message["channel"].decode("utf-8")
                all_sockets = self.rooms[room_id]
                for socket in all_sockets:
                    data = message["data"].decode("utf-8")
                    await socket.send_text(data)


_WebSocket = WebSocketManager()
