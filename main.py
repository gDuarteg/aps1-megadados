from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uuid

app = FastAPI()

class Task(BaseModel):
    description: str
    status: bool

db = {}

# test status
@app.get("/")
def read_root():
    return {"status": "running"}

# Get all db
@app.get("/tasks")
def read_db():
    return db

# Create Task
@app.post("/task/")
def create_task(task: Task):
    task_id = str(uuid.uuid1())
    db[task_id] = {
        'description': task.description,
        'status': task.status
    }
    return {"task_id": task_id}

# Read Task
@app.get("/task/{item_id}")
def read_task(task_id: str):
    if len(db) <= 0:
        return 'db is empty'
    else:
        try:
            return {"task": db[task_id]}
        except:
            return 'id not found'

# Update Task
@app.put("/task/{item_id}")
def update_task(task_id: str, task: Task):
    if len(db) <= 0:
        return 'db is empty'
    else:
        try:
            db[task_id]['status'] = task.status
            db[task_id]['description'] = task.description
            return {"task": db[task_id]}
        except:
            return 'id not found'

# Delete Task
@app.delete("/task/{item_id}")
def delete_task(task_id: str):
    if len(db) <= 0:
        return 'db is empty'
    else:
        try:
            del db[task_id]
            return 'task deleted'
        except:
            return 'id not found'
