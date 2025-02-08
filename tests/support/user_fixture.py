from app.user.domain.entity.user import User, UserOauth
from app.user.domain.vo import OauthProviderTypeEnum


def make_user(
    id: int = 1,
    password: str | None = "password",
    email: str = "survey@ding.dong",
    username: str = "dingdong-survey",
    is_admin: bool = False,
) -> User:
    user = User(
        password=password,
        email=email,
        username=username,
        is_admin=is_admin,
        profile_color="#3F57FD",
    )
    user.id = id
    return user


def make_user_oauth(
    *,
    id: int = 1,
    user_id: int = 1,
    oauth_id: str,
    provider: OauthProviderTypeEnum = OauthProviderTypeEnum.GOOGLE,
) -> UserOauth:
    user_oauth = UserOauth(
        user_id=user_id,
        oauth_id=oauth_id,
        provider=provider,
    )
    user_oauth.id = id
    return user_oauth
