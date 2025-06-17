from app.api.schemas.todo import ToDoCreate, ToDoFromDB
from app.utils.unitofwork import UnitOfWork


class ToDoService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_todos(self) -> list[ToDoFromDB]:
        async with self.uow as uow:
            todos: list = await uow.todo.find_all()
            return [ToDoFromDB.model_validate(todo) for todo in todos]

    async def create_todo(self, todo: ToDoCreate) -> ToDoFromDB:
        todo_dict: dict = todo.model_dump()
        async with self.uow as uow:
            todo_from_db = await uow.todo.add_one(todo_dict)
            todo_to_return = ToDoFromDB.model_validate(todo_from_db)
            await uow.commit()
            return todo_to_return
