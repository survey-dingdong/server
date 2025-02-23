from typing import Any

import ujson

from app.user.domain.vo import LoginTypeEnum
from core.config import config
from core.constants import LOGIN_SESSION_PREFIX, REFRESH_TOKEN_PREFIX
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

    async def set(self, *, response: Any, key: str, ttl: int | None = None) -> None:
        if isinstance(response, dict):
            response = ujson.dumps(response)

        await redis_client.set(name=key, value=response, ex=ttl)

    async def delete(self, *, key: str) -> None:
        await redis_client.delete(key)

    async def delete_startswith(self, *, value: str) -> None:
        async for key in redis_client.scan_iter(f"{value}*"):
            await redis_client.delete(key)

    async def store_login_session(
        self, *, user_id: int, login_type: str, token: str
    ) -> None:
        other_type = (
            LoginTypeEnum.App if login_type == LoginTypeEnum.Web else LoginTypeEnum.Web
        )
        existing_key = f"{LOGIN_SESSION_PREFIX}::{other_type}::user::{user_id}"

        if await redis_client.exists(existing_key):
            await redis_client.delete(existing_key)

        new_key = f"{LOGIN_SESSION_PREFIX}::{login_type}::user::{user_id}"
        await self.set(
            response=token,
            key=new_key,
        )

    async def validate_login_session(
        self, *, user_id: int, login_type: str, token: str
    ) -> bool:
        key = f"{LOGIN_SESSION_PREFIX}::{login_type}::user::{user_id}"
        return str(await self.get(key=key)) == token

    async def store_refresh_token(self, *, user_id: int, value: str) -> None:
        refresh_token_key = f"{REFRESH_TOKEN_PREFIX}::user::{user_id}"

        if await redis_client.exists(refresh_token_key):
            await redis_client.delete(refresh_token_key)

        await self.set(
            response=value,
            key=refresh_token_key,
            ttl=config.REFRESH_TOKEN_TTL,
        )

    async def get_refresh_token(self, *, user_id: int) -> Any:
        refresh_token_key = f"{REFRESH_TOKEN_PREFIX}::user::{user_id}"

        return await self.get(key=refresh_token_key)
