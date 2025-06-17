from fastapi import APIRouter, Depends

from app.api.schemas.todo import ToDoCreate, ToDoFromDB
from app.services.todo_service import ToDoService
from app.utils.unitofwork import IUnitOfWork, UnitOfWork


todo_router = APIRouter(prefix="/todo", tags=["ToDo"])


async def get_todo_service(unit_of_work: IUnitOfWork = Depends(UnitOfWork)):
    return ToDoService(unit_of_work)


@todo_router.get("/", response_model=list[ToDoFromDB])
async def get_todos(todo_service: ToDoService = Depends(get_todo_service)):
    return await todo_service.get_todos()


@todo_router.post("/", response_model=ToDoFromDB)
async def create_todo(todo: ToDoCreate, todo_service: ToDoService = Depends(get_todo_service)):
    return await todo_service.create_todo(todo)
