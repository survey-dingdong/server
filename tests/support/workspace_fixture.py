from app.workspace.domain.entity.workspace import Workspace


def make_workspace(
    id: int | None = None,
    title: str = "workspace",
    order: int = 1,
):
    return Workspace(
        id=id,
        title=title,
        order=order,
    )
