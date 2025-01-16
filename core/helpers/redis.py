from redis import asyncio as redis

from core.config import config

redis_client = redis.from_url(
    url=f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}",
    decode_responses=True,
    auto_close_connection_pool=False,
)
