import abc

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio.session import AsyncSession


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError


class Repository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_all(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def add_one(self, data: dict):
        query = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(query)
        return result.scalar_one()
