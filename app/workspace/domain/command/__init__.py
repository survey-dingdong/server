from pydantic import BaseModel


class CreateWorkspaceCommand(BaseModel):
    title: str
