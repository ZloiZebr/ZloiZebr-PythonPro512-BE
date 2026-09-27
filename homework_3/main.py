from datetime import datetime
from enum import Enum
from fastapi import FastAPI,HTTPException, Path, status
from pydantic import BaseModel, Field
from typing import Annotated


app = FastAPI()

tasks_db = {
    1: {
        "id": 1,
        "title": "Do my homework",
        "description": "I need study well to be smart",
        "priority": "high",
        "created_at": "2026-09-27T18:11:21.510938"
    },
    2: {
        "id": 2,
        "title": "Have a fun",
        "description": "I must have a good rest, to be ready for the next week",
        "priority": "common",
        "created_at": "2026-09-27T18:11:23.510938"
    }
}

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
    tasks_db[new_id] = new_task
    return new_task

@app.get("/tasks")
async def get_all_tasks() -> dict:
    if tasks_db:
        return tasks_db
    else:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "There is no Tasks yet"
        )

@app.get("/tasks/{task_id}", response_model = TaskResponse)
def get_task(
    task_id: Annotated[int, Path(ge=1)]
) -> TaskResponse:
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return tasks_db[task_id]

@app.put("/tasks/{task_id}",response_model = TaskResponse)
async def task_update(
    task_id: int,
    task_update: TaskUpdate,
) -> TaskResponse:
    if task_id not in tasks_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    updated_task = task_update.model_dump()
    update_time = datetime.now()
    updated_task["id"] = task_id
    updated_task["created_at"] = update_time
    tasks_db[task_id] = updated_task
    return updated_task

@app.patch("/tasks/{task_id}", response_model = TaskResponse)
async def task_partial_update(
    task_id: int,
    task_partial_update: TaskPartialUpdate
) -> TaskResponse:
    if task_id not in tasks_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if task_partial_update.title is None and task_partial_update.description is None and task_partial_update.priority is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must update at least one field"
        )
    task_to_update = tasks_db[task_id]
    if task_partial_update.title is not None:
        task_to_update['title'] = task_partial_update.title
    if task_partial_update.description is not None:
        task_to_update['description'] = task_partial_update.description
    if task_partial_update.priority is not None:
        task_to_update['priority'] = task_partial_update.priority
    update_time = datetime.now()
    task_to_update["id"] = task_id
    task_to_update["created_at"] = update_time
    return task_to_update

@app.delete("/tasks/{task_id}", response_model = TaskResponse)
async def task_delete(
    task_id: int
) -> TaskResponse:
    if task_id not in tasks_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task to delete not found")
    return tasks_db.pop(task_id)