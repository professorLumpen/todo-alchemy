from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.api.schemas.todo import ToDoCreate
from app.db.models import ToDo


class ToDoRepository(ABC):
    @abstractmethod
    async def get_todos(self) -> list[ToDo]:
        pass

    @abstractmethod
    async def create_todo(self, todo_db: ToDoCreate) -> ToDo:
        pass


class SQLAlchemyToDoRepository(ToDoRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_todos(self) -> Sequence[ToDo]:
        result = await self.session.execute(select(ToDo))
        return result.scalars().all()

    async def create_todo(self, todo: ToDoCreate) -> ToDo:
        todo_db = ToDo(**todo.model_dump())
        self.session.add(todo_db)
        await self.session.commit()
        await self.session.refresh(todo_db)
        return todo_db
