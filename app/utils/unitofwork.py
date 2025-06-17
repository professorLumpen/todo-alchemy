import abc

from app.db.database import async_session_maker
from app.repositories.todo_repository import ToDoRepository


class IUnitOfWork(abc.ABC):
    todo: ToDoRepository

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    async def commit(self):
        raise NotImplementedError

    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(IUnitOfWork):
    def __init__(self):
        self.session_fabric = async_session_maker

    async def __aenter__(self):
        self.session = await self.session_fabric()
        self.todo = ToDoRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()
        await self.session.close()
        self.session = None

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
