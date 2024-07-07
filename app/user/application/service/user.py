from pydantic import SecretStr

from app.auth.domain.vo import EmailVerificationType
from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.application.dto import (
    CreateUserResponseDTO,
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
from app.user.domain.command import CreateUserCommand, UserOauthCommand
from app.user.domain.entity.user import User, UserOauth, UserRead
from app.user.domain.usecase.user import UserUseCase
from core.config import config
from core.db import Transactional
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

    async def get_user_list(self, page: int, size: int) -> list[UserRead]:
        users = await self.repository.get_users(page=page, size=size)
        return [UserRead.model_validate(user) for user in users]

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.repository.get_user_by_id(user_id=user_id)
        if user is None:
            raise UserNotFoundException

        return user

    @Transactional()
    async def create_user(self, command: CreateUserCommand) -> CreateUserResponseDTO:
        signup_code = await self.cache.get(
            key=f"{config.REDIS_KEY_PREFIX}::{EmailVerificationType.SIGNUP}::{command.email}"
        )
        if signup_code is None:
            raise UnauthorizedAccessException

        is_exist = await self.repository.get_user_by_email(email=command.email)
        if is_exist:
            raise DuplicateEmailOrusernameException

        user = User.create(
            email=command.email,
            username=command.username,
            password=generate_hashed_password(
                password=command.password.get_secret_value()
            ),
        )
        user = await self.repository.save(user=user, auto_flush=True)

        await self.cache.delete(
            key=f"{config.REDIS_KEY_PREFIX}::{EmailVerificationType.SIGNUP}::{command.email}"
        )

        return CreateUserResponseDTO(
            token=TokenHelper.encode(payload={"user_id:": user.id}),
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

        if user.is_admin is False:
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

        refresh_token_sub_value = make_random_string(16)
        await self.cache.delete(key=f"{config.REDIS_KEY_PREFIX}::{user.id}")

        response = LoginResponseDTO(
            token=TokenHelper.encode(payload={"user_id": user.id}),
            refresh_token=TokenHelper.encode(
                payload={"sub": refresh_token_sub_value},
                expire_period=config.REFRESH_TOKEN_TTL,
            ),
        )

        await self.cache.set(
            response=refresh_token_sub_value,
            key=f"{config.REDIS_KEY_PREFIX}::{user.id}",
            ttl=config.REFRESH_TOKEN_TTL,
        )

        return response

    @Transactional()
    async def oauth_login(self, command: UserOauthCommand) -> LoginResponseDTO:
        user = await self.repository.get_user_by_email(email=command.email)
        if user is None:
            new_user = User.create(
                email=command.email,
                username=command.username,
            )
            user = await self.repository.save(user=new_user, auto_flush=True)
            new_user_oauth = UserOauth.create(
                user_id=new_user.id,
                oauth_id=command.oauth_id,
                provider=command.provider,
            )
            await self.repository.save(new_user_oauth)
        elif user.password:
            raise UserAlreadyExistsException
        else:
            user_oauth = await self.repository.get_user_oauth_by_id(
                user_id=user.id, oauth_id=command.oauth_id
            )
            if user_oauth is None:
                raise UserNotFoundException

            if user_oauth.provider != command.provider:
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
