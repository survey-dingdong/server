from app.user.domain.entity.user import User


def make_user(
    id: int | None = None,
    password: str = "password",
    email: str = "survey@ding.dong",
    username: str = "survey-dingdong",
    is_admin: bool = False,
):
    return User(
        id=id,
        password=password,
        email=email,
        username=username,
        is_admin=is_admin,
    )
