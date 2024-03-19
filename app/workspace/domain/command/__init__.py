from pydantic import BaseModel


class CreateWorkspaceCommand(BaseModel):
    user_id: int
    title: str
