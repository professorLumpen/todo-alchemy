from datetime import datetime

from pydantic import BaseModel


class ToDoCreate(BaseModel):
    description: str
    completed: bool = False


class ToDoFromDB(ToDoCreate):
    id: int
    created_at: datetime
