from functools import wraps
from typing import Any, Callable, TypeVar

from .base import BaseBackend, BaseKeyMaker
from .cache_tag import CacheTag

T = TypeVar("T", bound=Callable[..., Any])


class CacheManager:
    def __init__(self) -> None:
        self.backend: BaseBackend | None = None
        self.key_maker: BaseKeyMaker | None = None

    def init(self, *, backend: BaseBackend, key_maker: BaseKeyMaker) -> None:
        self.backend = backend
        self.key_maker = key_maker

    def cached(
        self,
        *,
        prefix: str = "",
        tag: CacheTag | None = None,
        ttl: int = 60,
    ) -> Callable[[T], T]:
        def _cached(function):
            @wraps(function)
            async def __cached(*args, **kwargs):
                if self.backend is None or self.key_maker is None:
                    raise Exception("backend or key_maker is None")

                key = await self.key_maker.make(
                    function=function,
                    prefix=prefix if not prefix else tag.value,  # type: ignore[union-attr]
                )
                cached_response = await self.backend.get(key=key)
                if cached_response:
                    return cached_response

                response = await function(*args, **kwargs)
                await self.backend.set(response=response, key=key, ttl=ttl)
                return response

            return __cached

        return _cached

    async def remove_by_tag(self, *, tag: CacheTag) -> None:
        await self.backend.delete_startswith(value=tag.value)  # type: ignore[union-attr]

    async def remove_by_prefix(self, *, prefix: str) -> None:
        await self.backend.delete_startswith(value=prefix)  # type: ignore[union-attr]


Cache = CacheManager()
