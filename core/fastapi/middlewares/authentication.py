from typing import Any

import jwt
from pydantic import BaseModel
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from core.config import config


class CurrentUser(BaseModel):
    id: int | None = None


class AuthBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
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
            user_id = payload.get("user_id")
        except jwt.exceptions.PyJWTError:
            return False, current_user

        current_user.id = user_id
        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
