from app.user.domain.entity.user import User


def make_user(
    id: int | None = None,
    password: str = "password",
    email: str = "h@id.e",
    nickname: str = "hide",
    is_admin: bool = False,
):
    return User(
        id=id,
        password=password,
        email=email,
        nickname=nickname,
        is_admin=is_admin,
    )
