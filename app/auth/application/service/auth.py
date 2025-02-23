import asyncio
from typing import cast

from app.auth.adapter.output.external_system.external_system_adapter import (
    ExternalSystemAdapter,
)
from app.auth.application.dto import RefreshTokenResponseDTO
from app.auth.application.exception import DecodeTokenException, InvalidTokenException
from app.auth.domain.usecase.auth import AuthUseCase
from app.auth.domain.vo import EmailVerificationType
from app.user.domain.vo import LoginTypeEnum
from core.constants import EMAIL_VERIFICATION_PREFIX
from core.helpers.cache.base import BaseBackend
from core.helpers.token import TokenHelper
from core.helpers.utils import generate_random_digit_string


class AuthService(AuthUseCase):
    def __init__(self, port: ExternalSystemAdapter, cache: BaseBackend) -> None:
        self.port = port
        self.cache = cache

    async def refresh_access_token(
        self,
        access_token: str,
        refresh_token: str,
        login_type: LoginTypeEnum,
    ) -> RefreshTokenResponseDTO:
        decoded_refresh_token = TokenHelper.decode(token=refresh_token)

        decoded_access_token = TokenHelper.decode_ignore_exp(token=access_token)
        user_id = cast(int, decoded_access_token.get("user_id"))
        refresh_token_value = await self.cache.get_refresh_token(user_id=user_id)
        if decoded_refresh_token.get("sub") != refresh_token_value:
            raise DecodeTokenException

        return RefreshTokenResponseDTO(
            access_token=TokenHelper.encode(
                payload={"user_id": user_id, "login_type": login_type}
            ),
            refresh_token=TokenHelper.encode(payload={"sub": refresh_token_value}),
        )

    async def send_verification_email(
        self, email: str, verification_type: EmailVerificationType
    ) -> None:
        code = generate_random_digit_string()
        await self.cache.set(
            response=code,
            key=f"{EMAIL_VERIFICATION_PREFIX}::{verification_type}::email::{email}",
            ttl=300,
        )
        asyncio.create_task(
            self.port.send_email(
                email=email, code=code, verification_type=verification_type
            )
        )

    async def validate_verification_email(
        self, email: str, code: str, verification_type: EmailVerificationType
    ) -> None:
        cached_code = await self.cache.get(
            key=f"{EMAIL_VERIFICATION_PREFIX}::{verification_type}::email::{email}"
        )
        if str(cached_code) != code:
            raise InvalidTokenException
