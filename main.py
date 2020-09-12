from fastapi import FastAPI
from taskcontrol import get_router, create_router, update_router, delete_router

tags = [
    {
        "name": "state",
        "description": "Checks if API is running normally"
    },
    {
        "name": "get",
        "description": "Prints all tasks currently in database"
    },
    {
        "name": "filter_status",
        "description": "Finds all tasks with a given status"
    },
    {
        "name": "filter_id",
        "description": "Finds a task by a given ID"
    },
    {
        "name":"create",
        "description":"Method used to create a task"
    },    
    {
        "name": "update_status",
        "description": "Method used to update the task's status"
    },
    {
        "name": "update_desc",
        "description": "Method used to update the task's description"
    },
    {
        "name": "delete",
        "description": "Method used to delete a task"
    }
]

app = FastAPI(
    title='Task Management',
    description='Simple API built using FastAPI and Python to better view and manage your tasks',
    openapi_tags=tags
)

global db_tasks
db_tasks = {}

# test status
@app.get("/", tags=["state"])
def read_root():
    return {"status": "running"}

app.include_router(get_router)
app.include_router(create_router)
app.include_router(update_router)
app.include_router(delete_router)
