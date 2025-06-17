from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.api.schemas.todo import ToDoCreate, ToDoFromDB
from app.db.database import get_db
from app.db.models import ToDo


todo_router = APIRouter(prefix="/todo", tags=["ToDo"])


@todo_router.get("/", response_model=list[ToDoFromDB])
async def get_todos(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(ToDo))
    return result.scalars().all()


@todo_router.post("/", response_model=ToDoFromDB)
async def create_todo(todo: ToDoCreate, session: AsyncSession = Depends(get_db)):
    todo_db = ToDo(**todo.model_dump())
    session.add(todo_db)
    await session.commit()
    await session.refresh(todo_db)
    return todo_db
