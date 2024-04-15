from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.application.dto import LoginResponseDTO
from app.user.application.exception import (
    DuplicateEmailOrNicknameException,
    PasswordDoesNotMatchException,
    UserNotFoundException,
)
from app.user.domain.command import CreateUserCommand
from app.user.domain.entity.user import User, UserRead
from app.user.domain.usecase.user import UserUseCase
from core.db import Transactional
from core.helpers.auth import generate_hashed_password, validate_hashed_password
from core.helpers.token import TokenHelper


class UserService(UserUseCase):
    def __init__(self, repository: UserRepositoryAdapter):
        self.repository = repository

    async def get_user_list(self, page: int, size: int) -> list[UserRead]:
        return await self.repository.get_users(page=page, size=size)

    @Transactional()
    async def create_user(self, command: CreateUserCommand) -> None:
        if command.password1.get_secret_value() != command.password2.get_secret_value():
            raise PasswordDoesNotMatchException

        is_exist = await self.repository.get_user_by_email_or_nickname(
            email=command.email,
            nickname=command.nickname,
        )
        if is_exist:
            raise DuplicateEmailOrNicknameException

        user = User.create(
            email=command.email,
            password=generate_hashed_password(
                password=command.password1.get_secret_value()
            ),
            nickname=command.nickname,
        )
        await self.repository.save(user=user)

    async def is_admin(self, user_id: int) -> bool:
        user = await self.repository.get_user_by_id(user_id=user_id)
        if not user:
            return False

        if user.is_admin is False:
            return False

        return True

    async def login(self, email: str, password: str) -> LoginResponseDTO:
        user = await self.repository.get_user_by_email(email=email)
        if not user:
            raise UserNotFoundException

        if not validate_hashed_password(
            password=password, hashed_password=user.password
        ):
            raise PasswordDoesNotMatchException

        response = LoginResponseDTO(
            token=TokenHelper.encode(payload={"user_id": user.id}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )
        return response
