# API imports
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid1, UUID
from enum import Enum

# imports from other files
from task import Task
import main


# Router to get all tasks, filter tasks by status or find a specific task
get_router = APIRouter()

# Class used to control a task's status
class TaskStatus(str, Enum):
    COMPLETE = "complete",
    PENDING = "pending"


@get_router.get("/tasks", tags=["get"])
def list_tasks():
    return {"tasks": main.db_tasks}


@get_router.get("/tasks/status/{task_status}", tags=["filter_status"])
def filter_status(task_status: TaskStatus):
    filtered = {}
    
    if task_status == TaskStatus.COMPLETE:
        task_status = True

    elif task_status == TaskStatus.PENDING:
        task_status = False

    for k, v in main.db_tasks.items():
        if v.status == task_status:
            filtered[k] = v

    return {"filtered_tasks": filtered}


@get_router.get("/tasks/id/{task_id}", tags=["filter_id"])
def filter_id(task_id: UUID):
    if not task_id in main.db_tasks:
        raise HTTPException(status_code=404, detail="Task not found!")

    else:
        return {"task": main.db_tasks[task_id]}


# Router to create a new task
create_router = APIRouter()

@create_router.post("/new_task", tags=["create"])
def create_task(description: str):
    task_id = uuid1()
    new_task = Task(description=description, status=False)
    main.db_tasks[task_id] = new_task

    return {"task_id":task_id}


# Router to update a task
update_router = APIRouter()

# Class used to update a task
class TaskBody(BaseModel):
    task_id: Optional[UUID] = Field(None, title="Task ID")
    description: Optional[str] = Field(None, title="Task description")
    status: Optional[bool] = Field(None, title="Current status of the task")
    

@update_router.patch("/task/status", tags=["update_status"])
def update_status(body: TaskBody):
    task_id = body.task_id
    status = body.status

    if status == None:
        raise HTTPException(status_code=422, detail="Status is empty!")

    elif not task_id in main.db_tasks:
        raise HTTPException(status_code=404, detail="Task not found!")

    else:
        main.db_tasks[task_id].status = status
        return {"status_updated": True}


@update_router.patch("/task/description", tags=["update_desc"])
def update_description(body: TaskBody):
    task_id = body.task_id
    description = body.description

    if description == None:
        raise HTTPException(status_code=422, detail="Description is empty!")

    elif not task_id in main.db_tasks:
        raise HTTPException(status_code=404, detail="Task not found!")

    else:
        main.db_tasks[task_id].description = description
        return {"description_updated": True}

# Router to delete a task

delete_router = APIRouter()

@delete_router.delete("/task/{id}", tags=["delete"])
def delete_task(task_id: UUID):
    if not task_id in main.db_tasks:
        raise HTTPException(status_code=404, detail="Task not found!")

    else:
        del main.db_tasks[task_id]
        return {"task_deleted":True}
