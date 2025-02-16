from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.auth.adapter.input.api.v1.request import (
    EmailVerificationRequest,
    RefreshTokenRequest,
    ResetPasswordRequest,
    VerifyEmailRequest,
)
from app.auth.application.dto import RefreshTokenResponseDTO, ValidateEmailResponseDTO
from app.auth.container import AuthContainer
from app.auth.domain.usecase.auth import AuthUseCase
from app.auth.domain.vo import EmailVerificationType
from app.user.container import UserContainer
from app.user.domain.usecase.user import UserUseCase

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(
    "/refresh",
    response_model=RefreshTokenResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def refresh_token(
    request: RefreshTokenRequest,
    auth_usecase: AuthUseCase = Depends(Provide[AuthContainer.auth_service]),
) -> RefreshTokenResponseDTO:
    return await auth_usecase.create_refresh_token(
        token=request.token, refresh_token=request.refresh_token
    )


@auth_router.post(
    "/email-availability",
    response_model=ValidateEmailResponseDTO,
)
@inject
async def check_email_availability(
    request: EmailVerificationRequest,
    user_usecase: UserUseCase = Depends(Provide[UserContainer.user_service]),
) -> ValidateEmailResponseDTO:
    availability = await user_usecase.is_email_available(email=request.email)
    return ValidateEmailResponseDTO(availability=availability)


@auth_router.post(
    "/email-verifications",
)
@inject
async def send_verification_email(
    request: EmailVerificationRequest,
    verification_type: EmailVerificationType,
    auth_usecase: AuthUseCase = Depends(Provide[AuthContainer.auth_service]),
) -> None:
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
    auth_usecase: AuthUseCase = Depends(Provide[AuthContainer.auth_service]),
) -> None:
    await auth_usecase.validate_verification_email(
        email=request.email,
        code=request.code,
        verification_type=verification_type,
    )


@auth_router.post(
    "/reset-password",
)
@inject
async def reset_password(
    request: ResetPasswordRequest,
    user_usecase: UserUseCase = Depends(Provide[UserContainer.user_service]),
) -> None:
    await user_usecase.reset_password(
        email=request.email, new_password=request.password
    )
