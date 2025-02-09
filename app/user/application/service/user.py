from pydantic import SecretStr

from app.auth.domain.vo import EmailVerificationType
from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.application.dto import (
    CreateUserResponseDTO,
    GetUserListResponseDTO,
    GetUserResponseDTO,
    LoginResponseDTO,
    UpdateUserRequestDTO,
)
from app.user.application.exception import (
    DifferentOAuthProviderException,
    DuplicateEmailOrusernameException,
    OAuthLoginWithPasswordAttemptException,
    PasswordDoesNotMatchException,
    PasswordNotChangedException,
    UnauthorizedAccessException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.user.domain.entity.user import User, UserOauth
from app.user.domain.usecase.user import UserUseCase
from app.user.domain.vo import OauthProviderTypeEnum
from core.config import config
from core.db import Transactional
from core.exceptions.base import InvalidAccessException
from core.helpers.auth import (
    generate_hashed_password,
    make_random_string,
    validate_hashed_password,
)
from core.helpers.cache.base.backend import BaseBackend
from core.helpers.token import TokenHelper


class UserService(UserUseCase):
    def __init__(self, repository: UserRepositoryAdapter, cache: BaseBackend):
        self.repository = repository
        self.cache = cache

    async def is_email_available(self, email: str) -> bool:
        user = await self.repository.get_user_by_email(email=email)
        if user is None:
            return True

        return False

    async def get_user_list(self, page: int, size: int) -> list[GetUserListResponseDTO]:
        users = await self.repository.get_users(page=page, size=size)

        user_id_to_oauth_accounts = {}
        if users:
            user_ids = [user.id for user in users]
            user_id_to_oauth_accounts = await self.repository.get_user_oauth_accounts(
                user_ids
            )

        return [
            GetUserListResponseDTO(
                id=user.id,
                email=user.email,
                username=user.username,
                is_admin=user.is_admin,
                is_deleted=user.is_deleted,
                oauth_accounts=user_id_to_oauth_accounts.get(user.id, []),
            )
            for user in users
        ]

    async def get_user_by_id(self, user_id: int) -> GetUserResponseDTO:
        user = await self.repository.get_user_by_id(user_id=user_id)
        if user is None:
            raise UserNotFoundException

        user_id_to_oauth_accounts = await self.repository.get_user_oauth_accounts(
            [user_id]
        )

        return GetUserResponseDTO(
            id=user.id,
            email=user.email,
            username=user.username,
            oauth_accounts=user_id_to_oauth_accounts.get(user.id, []),
        )

    @Transactional()
    async def create_user(
        self, email: str, username: str, password: SecretStr
    ) -> CreateUserResponseDTO:
        signup_code = await self.cache.get(
            key=f"{config.REDIS_KEY_PREFIX}::{EmailVerificationType.SIGNUP}::{email}"
        )
        if signup_code is None:
            raise UnauthorizedAccessException

        user = await self.repository.get_user_by_email(email=email)
        if user is not None:
            raise DuplicateEmailOrusernameException

        user = User(
            email=email,
            username=username,
            password=generate_hashed_password(password=password.get_secret_value()),
        )

        await self.repository.add(user=user, auto_flush=True)

        await self.cache.delete(
            key=f"{config.REDIS_KEY_PREFIX}::{EmailVerificationType.SIGNUP}::{email}"
        )

        return CreateUserResponseDTO(
            token=TokenHelper.encode(payload={"user_id": user.id}),
        )

    @Transactional()
    async def update_user(self, user_id: int, user_dto: UpdateUserRequestDTO) -> None:
        user = await self.repository.get_user_by_id(user_id=user_id)
        if user is None:
            raise UserNotFoundException

        for column, value in user_dto.model_dump(exclude_unset=True).items():
            setattr(user, column, value)

    @Transactional()
    async def delete_user(self, user_id: int) -> None:
        user = await self.repository.get_user_by_id(user_id=user_id)
        if user is None:
            raise UserNotFoundException

        user.is_deleted = True

    async def is_admin(self, user_id: int) -> bool:
        user = await self.repository.get_user_by_id(user_id=user_id)
        if user is None:
            return False

        if not user.is_admin:
            return False

        return True

    async def login(self, email: str, password: SecretStr) -> LoginResponseDTO:
        user = await self.repository.get_user_by_email(email=email)
        if user is None:
            raise UserNotFoundException

        if user.password is None:
            raise OAuthLoginWithPasswordAttemptException

        if not validate_hashed_password(
            password=password.get_secret_value(), hashed_password=user.password
        ):
            raise PasswordDoesNotMatchException

        await self.cache.delete(key=f"{config.REDIS_KEY_PREFIX}::{user.id}")

        refresh_token_sub_value = make_random_string(16)

        await self.cache.set(
            response=refresh_token_sub_value,
            key=f"{config.REDIS_KEY_PREFIX}::{user.id}",
            ttl=config.REFRESH_TOKEN_TTL,
        )

        return LoginResponseDTO(
            token=TokenHelper.encode(payload={"user_id": user.id}),
            refresh_token=TokenHelper.encode(
                payload={"sub": refresh_token_sub_value},
                expire_period=config.REFRESH_TOKEN_TTL,
            ),
        )

    @Transactional()
    async def oauth_login(
        self,
        email: str,
        username: str,
        provider: OauthProviderTypeEnum,
        oauth_id: str,
    ) -> LoginResponseDTO:
        user = await self.repository.get_user_by_email(email=email)
        if user is None:
            new_user = User(
                email=email,
                password=None,
                username=username,
            )
            user = await self.repository.add(user=new_user, auto_flush=True)

        if user.password is not None:
            raise UserAlreadyExistsException

        user_oauth = await self.repository.get_user_by_oauth_id(
            user_id=user.id, oauth_id=oauth_id
        )
        if user_oauth is None:
            user_oauth = UserOauth(
                user_id=user.id,
                oauth_id=oauth_id,
                provider=provider,
            )

        if user_oauth.provider != provider:
            raise DifferentOAuthProviderException

        response = LoginResponseDTO(
            token=TokenHelper.encode(payload={"user_id": user.id}),
            refresh_token=TokenHelper.encode(
                payload={"sub": make_random_string(16)},
                expire_period=config.REFRESH_TOKEN_TTL,
            ),
        )
        return response

    @Transactional()
    async def change_password(
        self, user_id: int, old_password: SecretStr, new_password: SecretStr
    ) -> None:
        user = await self.repository.get_user_by_id(user_id=user_id)
        if user is None:
            raise UserNotFoundException

        if user.password is None:
            raise InvalidAccessException

        if not validate_hashed_password(
            password=old_password.get_secret_value(), hashed_password=user.password
        ):
            raise PasswordDoesNotMatchException

        if old_password.get_secret_value() == new_password.get_secret_value():
            raise PasswordNotChangedException

        user.password = generate_hashed_password(
            password=new_password.get_secret_value()
        )

    @Transactional()
    async def reset_password(self, email: str, new_password: SecretStr) -> None:
        user = await self.repository.get_user_by_email(email=email)
        if user is None:
            raise UserNotFoundException

        cached_code = await self.cache.get(
            key=f"{config.REDIS_KEY_PREFIX}::{EmailVerificationType.RESET_PASSWORD}::{email}"
        )
        if cached_code is None:
            raise UnauthorizedAccessException

        user.password = generate_hashed_password(
            password=new_password.get_secret_value()
        )

        await self.cache.delete(
            key=f"{config.REDIS_KEY_PREFIX}::{EmailVerificationType.RESET_PASSWORD}::{email}"
        )
