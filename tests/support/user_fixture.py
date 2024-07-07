from app.user.domain.entity.user import User, UserOauth
from app.user.domain.vo import OauthProviderTypeEnum


def make_user(
    id: int | None = None,
    password: str | None = "password",
    email: str = "survey@ding.dong",
    username: str = "dingdong-survey",
    is_admin: bool = False,
):
    return User(
        id=id,
        password=password,
        email=email,
        username=username,
        is_admin=is_admin,
    )


def make_user_oauth(
    id: int | None = None,
    user_id: int | None = None,
    oauth_id: str | None = None,
    provider: OauthProviderTypeEnum = OauthProviderTypeEnum.GOOGLE,
):
    return UserOauth(
        id=id,
        user_id=user_id,
        oauth_id=oauth_id,
        provider=provider,
    )
