from pydantic import SecretStr

from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.application.dto import (
    CreateUserResponseDTO,
    LoginResponseDTO,
    UpdateUserRequestDTO,
)
from app.user.application.exception import (
    DuplicateEmailOrusernameException,
    PasswordDoesNotMatchException,
    PasswordNotChangedException,
    UserNotFoundException,
)
from app.user.domain.command import CreateUserCommand
from app.user.domain.entity.user import User, UserRead
from app.user.domain.usecase.user import UserUseCase
from core.config import config
from core.db import Transactional
from core.helpers.auth import (
    generate_hashed_password,
    make_random_string,
    validate_hashed_password,
)
from core.helpers.cache import RedisBackend
from core.helpers.token import TokenHelper

redis_backend = RedisBackend()


class UserService(UserUseCase):
    def __init__(self, repository: UserRepositoryAdapter):
        self.repository = repository

    async def validate_email(self, email: str) -> bool:
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
        is_exist = await self.repository.get_user_by_email_or_username(
            email=command.email,
            username=command.username,
        )
        if is_exist:
            raise DuplicateEmailOrusernameException

        user = User.create(
            email=command.email,
            password=generate_hashed_password(
                password=command.password.get_secret_value()
            ),
            username=command.username,
        )
        user = await self.repository.save(user=user, auto_flush=True)

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

        if not validate_hashed_password(
            password=password.get_secret_value(), hashed_password=user.password
        ):
            raise PasswordDoesNotMatchException

        refresh_token_sub_value = make_random_string(16)
        await redis_backend.delete(key=f"{config.REDIS_KEY_PREFIX}::{user.id}")
        response = LoginResponseDTO(
            token=TokenHelper.encode(payload={"user_id": user.id}),
            refresh_token=TokenHelper.encode(
                payload={"sub": refresh_token_sub_value},
                expire_period=config.REFRESH_TOKEN_TTL,
            ),
        )
        await redis_backend.set(
            response=refresh_token_sub_value,
            key=f"{config.REDIS_KEY_PREFIX}::{user.id}",
            ttl=config.REFRESH_TOKEN_TTL,
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
