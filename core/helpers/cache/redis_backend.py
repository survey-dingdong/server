from typing import Any

import ujson

from core.helpers.cache.base import BaseBackend
from core.helpers.redis import redis_client


class RedisBackend(BaseBackend):
    async def get(self, *, key: str) -> Any:
        data = await redis_client.get(key)
        if not data:
            return

        try:
            result = ujson.loads(data)
        except ujson.JSONDecodeError:
            result = data
        return result

    async def set(self, *, response: Any, key: str, ttl: int = 60) -> None:
        if isinstance(response, dict):
            response = ujson.dumps(response)

        await redis_client.set(name=key, value=response, ex=ttl)

    async def delete(self, *, key: str) -> None:
        await redis_client.delete(key)

    async def delete_startswith(self, *, value: str) -> None:
        async for key in redis_client.scan_iter(f"{value}*"):
            await redis_client.delete(key)
