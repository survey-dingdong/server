from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import EmailStr

from app.auth.adapter.input.api.v1.request import RefreshTokenRequest
from app.auth.adapter.input.api.v1.response import RefreshTokenResponse
from app.auth.container import Container
from app.auth.domain.usecase.auth import AuthUseCase

auth_router = APIRouter()


@auth_router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
)
@inject
async def refresh_token(
    request: RefreshTokenRequest,
    usecase: AuthUseCase = Depends(Provide[Container.auth_service]),
):
    token = await usecase.create_refresh_token(
        token=request.token, refresh_token=request.refresh_token
    )
    return {"token": token.token, "refresh_token": token.refresh_token}


@auth_router.post(
    "/email-validation",
)
@inject
async def send_email(
    email: EmailStr,
    usecase: AuthUseCase = Depends(Provide[Container.auth_service]),
):
    await usecase.send_email(email=email)
