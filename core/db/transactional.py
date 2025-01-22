from functools import wraps
from typing import Awaitable, Callable, TypeVar

from core.db import session

T = TypeVar("T")


class Transactional:
    def __call__(
        self, func: Callable[..., Awaitable[T]]
    ) -> Callable[..., Awaitable[T]]:
        @wraps(func)
        async def _transactional(*args, **kwargs) -> T:  # type: ignore
            try:
                result = await func(*args, **kwargs)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e

            return result

        return _transactional
