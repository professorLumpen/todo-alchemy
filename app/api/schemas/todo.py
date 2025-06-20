from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ToDoCreate(BaseModel):
    description: str
    completed: bool = False


class ToDoFromDB(ToDoCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
