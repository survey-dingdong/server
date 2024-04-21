from app.auth.application.dto import RefreshTokenResponseDTO
from app.auth.application.exception import DecodeTokenException
from app.auth.domain.usecase.jwt import JwtUseCase
from core.config import config
from core.helpers.cache import RedisBackend
from core.helpers.token import DecodeTokenException as JwtDecodeTokenException
from core.helpers.token import ExpiredTokenException as JwtExpiredTokenException
from core.helpers.token import TokenHelper

redis_backend = RedisBackend()


class JwtService(JwtUseCase):
    async def verify_token(self, token: str) -> None:
        try:
            TokenHelper.decode(token=token)
        except (JwtDecodeTokenException, JwtExpiredTokenException):
            raise DecodeTokenException

    async def create_refresh_token(
        self,
        token: str,
        refresh_token: str,
    ) -> RefreshTokenResponseDTO:
        decoede_created_token = TokenHelper.decode_expired_token(token=token)
        decoded_refresh_token = TokenHelper.decode(token=refresh_token)

        user_id = decoede_created_token.get("user_id")
        refresh_token_sub_value = await redis_backend.get(
            key=f"{config.REDIS_KEY_PREFIX}::{user_id}"
        )
        if decoded_refresh_token.get("sub") != refresh_token_sub_value:
            raise DecodeTokenException

        return RefreshTokenResponseDTO(
            token=TokenHelper.encode(payload={"user_id": user_id}),
            refresh_token=TokenHelper.encode(payload={"sub": refresh_token_sub_value}),
        )
