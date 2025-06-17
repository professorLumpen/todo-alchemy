from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.api.schemas.todo import ToDoCreate, ToDoFromDB
from app.db.database import get_db
from app.repositories.todo_repository import SQLAlchemyToDoRepository, ToDoRepository


todo_router = APIRouter(prefix="/todo", tags=["ToDo"])


async def get_todo_repository(session: AsyncSession = Depends(get_db)):
    return SQLAlchemyToDoRepository(session)


@todo_router.get("/", response_model=list[ToDoFromDB])
async def get_todos(todo_repo: ToDoRepository = Depends(get_todo_repository)):
    return await todo_repo.get_todos()


@todo_router.post("/", response_model=ToDoFromDB)
async def create_todo(todo: ToDoCreate, todo_repo: ToDoRepository = Depends(get_todo_repository)):
    return await todo_repo.create_todo(todo)
