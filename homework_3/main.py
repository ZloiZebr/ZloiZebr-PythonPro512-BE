from datetime import datetime
from enum import Enum
from fastapi import Body, FastAPI,HTTPException, Path, status
from pydantic import BaseModel, ConfigDict, Field, StrictInt, field_validator
from typing import Annotated


app = FastAPI()

tasks_db = {}

class PriorityLevel(str, Enum):
    LOW = "low" 
    COMMON = "common"
    HIGH = "high"
    URGENT = "urgent"

# СХЕМЫ:
class TaskCreate(BaseModel):
    title: Annotated[str, Field(max_length = 50)]
    description: str
    priority: PriorityLevel

TaskUpdate = TaskCreate

class TaskPartialUpdate(BaseModel):
    title: Annotated[str|None, Field(max_length = 50)] = None
    description: str|None = None
    priority: PriorityLevel|None = None

class TaskResponse(BaseModel):
    model_config = ConfigDict(strict=True)
    id: Annotated[int, Field(ge = 1)]
    title: Annotated[str, Field(max_length = 50)]
    description: str
    priority: PriorityLevel
    created_at: datetime

# Эндпоинты:

@app.post("/tasks", status_code = status.HTTP_201_CREATED)
async def create_task(task_create:TaskCreate) -> TaskResponse: 
    new_id = max(tasks_db) + 1 if tasks_db else 1
    create_time = datetime.now()
    new_task = {
        "id": new_id,
        "title": task_create.title,
        "description": task_create.description, 
        "priority": task_create.priority,
        "created_at": create_time
    }
    return new_task

@app.get("/tasks")
async def get_all_tasks() -> dict[int:TaskResponse]: доделать формат ответа
    if tasks_db:
        return tasks_db
    else:
        raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "There is no Tasks yet"
    )

