from pydantic import BaseModel


class CreateProjectCommand(BaseModel):
    workspace_id: int
    title: str
