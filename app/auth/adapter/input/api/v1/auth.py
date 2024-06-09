from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.auth.adapter.input.api.v1.request import (
    EmailVerificationRequest,
    RefreshTokenRequest,
    VerifyEmailRequest,
)
from app.auth.adapter.input.api.v1.response import (
    RefreshTokenResponse,
    ValidateEmailResponse,
)
from app.auth.container import Container
from app.auth.domain.usecase.auth import AuthUseCase
from app.auth.domain.vo import EmailVerificationType
from app.user.container import UserContainer
from app.user.domain.usecase.user import UserUseCase

auth_router = APIRouter()


@auth_router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def refresh_token(
    request: RefreshTokenRequest,
    auth_usecase: AuthUseCase = Depends(Provide[Container.auth_service]),
):
    token = await auth_usecase.create_refresh_token(
        token=request.token, refresh_token=request.refresh_token
    )
    return RefreshTokenResponse(token=token.token, refresh_token=token.refresh_token)


@auth_router.post(
    "/email-availability",
)
@inject
async def check_email_availability(
    request: EmailVerificationRequest,
    user_usecase: UserUseCase = Depends(Provide[UserContainer.user_service]),
):
    availability = await user_usecase.validate_email(email=request.email)
    return ValidateEmailResponse(availability=availability)


@auth_router.post(
    "/email-verifications",
)
@inject
async def send_verification_email(
    request: EmailVerificationRequest,
    verification_type: EmailVerificationType,
    auth_usecase: AuthUseCase = Depends(Provide[Container.auth_service]),
):
    await auth_usecase.send_verification_email(
        email=request.email, verification_type=verification_type
    )


@auth_router.post(
    "/email-verifications/validation",
)
@inject
async def validate_verification_email(
    request: VerifyEmailRequest,
    verification_type: EmailVerificationType,
    auth_usecase: AuthUseCase = Depends(Provide[Container.auth_service]),
):
    await auth_usecase.validate_verification_email(
        email=request.email,
        code=request.code,
        verification_type=verification_type,
    )
