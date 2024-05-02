from app.workspace.domain.entity.workspace import Workspace


def make_workspace(
    id: int,
    user_id: int = 1,
    title: str = "workspace",
    order_no: int = 1,
    is_deleted: bool = False,
):
    return Workspace(
        id=id,
        user_id=user_id,
        title=title,
        order_no=order_no,
        is_deleted=is_deleted,
    )
