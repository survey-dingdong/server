from datetime import datetime

from app.project.domain.entity.experiment import ExperimentProject
from app.project.domain.vo.type import ProjectTypeEnum


def make_project(
    id: int,
    workspace_id: int = 1,
    title: str = "project",
    project_type: ProjectTypeEnum = ProjectTypeEnum.EXPERIMENT,
    is_public: bool | None = False,
    max_participants: int | None = 0,
    created_at: datetime | None = datetime.now(),
    updated_at: datetime | None = datetime.now(),
):
    return ExperimentProject(
        id=id,
        workspace_id=workspace_id,
        title=title,
        project_type=project_type,
        is_public=is_public,
        max_participants=max_participants,
        created_at=created_at,
        updated_at=updated_at,
    )
