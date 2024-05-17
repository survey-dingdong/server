from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query, Request

from app.user.adapter.input.api.v1.request import (
    ChangePasswordRequest,
    CreateUserRequest,
    LoginRequest,
)
from app.user.adapter.input.api.v1.response import (
    CreateUserResponse,
    GetUserListResponse,
    LoginResponse,
)
from app.user.container import UserContainer
from app.user.domain.command import CreateUserCommand
from app.user.domain.usecase.user import UserUseCase
from core.fastapi.dependencies import IsAdmin, IsAuthenticated, PermissionDependency

user_router = APIRouter()


@user_router.get(
    "",
    response_model=list[GetUserListResponse],
    dependencies=[Depends(PermissionDependency([IsAdmin]))],
)
@inject
async def get_user_list(
    page: int = Query(default=1),
    size: int = Query(default=10),
    usecase: UserUseCase = Depends(Provide[UserContainer.user_service]),
):
    return await usecase.get_user_list(page=page, size=size)


@user_router.get(
    "/me",
    response_model=GetUserListResponse,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def get_user_me(
    auth_info: Request,
    usecase: UserUseCase = Depends(Provide[UserContainer.user_service]),
):
    return await usecase.get_user_by_id(user_id=auth_info.user.id)


@user_router.post(
    "",
    response_model=CreateUserResponse,
)
@inject
async def create_user(
    request: CreateUserRequest,
    usecase: UserUseCase = Depends(Provide[UserContainer.user_service]),
):
    command = CreateUserCommand(**request.model_dump())
    return await usecase.create_user(command=command)


@user_router.post(
    "/login",
    response_model=LoginResponse,
)
@inject
async def login(
    request: LoginRequest,
    usecase: UserUseCase = Depends(Provide[UserContainer.user_service]),
):
    token = await usecase.login(email=request.email, password=request.password)
    return {"token": token.token, "refresh_token": token.refresh_token}


@user_router.patch(
    "/password",
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def change_password(
    auth_info: Request,
    request: ChangePasswordRequest,
    usecase: UserUseCase = Depends(Provide[UserContainer.user_service]),
):
    await usecase.change_password(
        user_id=auth_info.user.id,
        old_password=request.old_password,
        new_password=request.new_password,
    )
