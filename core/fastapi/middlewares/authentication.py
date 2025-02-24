from typing import Any

import jwt
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from pydantic import BaseModel
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from app.user.domain.vo import LoginTypeEnum
from core.config import config
from core.container import CoreContainer
from core.helpers.cache.redis_backend import RedisBackend


class CurrentUser(BaseModel):
    id: int | None = None
    login_type: LoginTypeEnum | None = None


class AuthBackend(AuthenticationBackend):
    @inject
    async def authenticate(
        self,
        conn: HTTPConnection,
        redis_client: RedisBackend = Depends(Provide[CoreContainer.redis_backend]),
    ) -> tuple[bool, CurrentUser | None]:
        current_user = CurrentUser()

        authorization: str | None = conn.headers.get("Authorization")
        if authorization is None:
            return False, current_user

        try:
            scheme, credentials = authorization.split(" ")
            if scheme.lower() != "bearer":
                return False, current_user
        except ValueError:
            return False, current_user

        if not credentials:
            return False, current_user

        try:
            payload: dict[str, Any] = jwt.decode(
                credentials,
                config.JWT_SECRET_KEY,
                algorithms=[config.JWT_ALGORITHM],
            )
        except jwt.exceptions.PyJWTError:
            return False, current_user

        current_user.id = payload.get("user_id")
        current_user.login_type = payload.get("login_type")

        if current_user.id is None or current_user.login_type is None:
            return False, current_user

        is_valid = await redis_client.validate_login_session(
            user_id=current_user.id,
            login_type=current_user.login_type,
            token=credentials,
        )

        if not is_valid:
            return False, current_user

        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
