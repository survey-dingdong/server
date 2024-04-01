from datetime import date, datetime

from app.project.domain.entity.experiment import ExperimentProject
from app.project.domain.vo.type import ExperimentTypeEnum


def make_experiment_project(
    id: int,
    workspace_id: int = 1,
    title: str = "project",
    description: str | None = None,
    is_public: bool | None = False,
    max_participants: int | None = 0,
    start_date: date | None = datetime.now().date(),
    end_date: date | None = datetime.now().date(),
    excluded_dates: list[str] | None = [],
    experiment_type: ExperimentTypeEnum | None = ExperimentTypeEnum.OFFLINE,
    location: str | None = "location",
    created_at: datetime | None = datetime.now(),
    updated_at: datetime | None = datetime.now(),
):
    return ExperimentProject(
        id=id,
        workspace_id=workspace_id,
        title=title,
        description=description,
        is_public=is_public,
        max_participants=max_participants,
        start_date=start_date,
        end_date=end_date,
        excluded_dates=excluded_dates,
        experiment_type=experiment_type,
        location=location,
        created_at=created_at,
        updated_at=updated_at,
    )
