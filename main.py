import uvicorn
from fastapi import FastAPI

from app.api.endpoints.todo import todo_router


app = FastAPI()
app.include_router(todo_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
