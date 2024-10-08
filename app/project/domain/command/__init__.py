from pydantic import BaseModel

from app.project.domain.vo import ProjectTypeEnum


class CreateProjectCommand(BaseModel):
    workspace_id: int
    title: str
    project_type: ProjectTypeEnum
