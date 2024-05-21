from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.auth.adapter.input.api.v1.request import (
    CreateEmailVerificationRequest,
    RefreshTokenRequest,
    VerifyEmailRequest,
)
from app.auth.adapter.input.api.v1.response import RefreshTokenResponse
from app.auth.container import Container
from app.auth.domain.usecase.auth import AuthUseCase

auth_router = APIRouter()


@auth_router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def refresh_token(
    request: RefreshTokenRequest,
    usecase: AuthUseCase = Depends(Provide[Container.auth_service]),
):
    token = await usecase.create_refresh_token(
        token=request.token, refresh_token=request.refresh_token
    )
    return RefreshTokenResponse(token=token.token, refresh_token=token.refresh_token)


@auth_router.post(
    "/email-verifications",
)
@inject
async def create_email_verification(
    request: CreateEmailVerificationRequest,
    usecase: AuthUseCase = Depends(Provide[Container.auth_service]),
):
    await usecase.send_email(email=request.email)


@auth_router.post(
    "/email-verifications/verify",
)
@inject
async def verify_email(
    request: VerifyEmailRequest,
    usecase: AuthUseCase = Depends(Provide[Container.auth_service]),
):
    await usecase.verify_email(email=request.email, code=request.code)
