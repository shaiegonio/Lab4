from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, Field
from typing import List
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
APIKey = APIKeyHeader(name="X-API-Key")

app = FastAPI()

task_db_v1 = [
    {"task_id": 1, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 4", "is_finished": False}
]

task_db_v2 = []

class Task(BaseModel):
    task_title: str = Field(..., min_length=1)
    task_desc: str = Field(..., min_length=1)
    is_finished: bool = False


def get_task_by_id(task_id: int, task_db: List[dict]):
    return next((task for task in task_db if task["task_id"] == task_id), None)

def validate_api_key(api_key: str = Depends(APIKey)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

# API Version 1 Endpoints
@app.get("/apiv1/tasks/{task_id}")
def fetch_task_v1(task_id: int):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid task ID. Must be greater than 0.")
    
    task = get_task_by_id(task_id, task_db_v1)
    if task is None:
        raise HTTPException(status_code=404, detail=f"No task found with id {task_id}")
    
    return {"status": "ok", "task": task}

@app.post("/apiv1/tasks")
def add_task_v1(task: Task):
    new_task_id = len(task_db_v1) + 1
    new_task = {
        "task_id": new_task_id,
        "task_title": task.task_title,
        "task_desc": task.task_desc,
        "is_finished": task.is_finished
    }
    task_db_v1.append(new_task)
    return {"status": "ok", "task": new_task}

@app.delete("/apiv1/tasks/{task_id}")
def remove_task_v1(task_id: int):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid task ID. Must be greater than 0.")
    
    task = get_task_by_id(task_id, task_db_v1)
    if not task:
        raise HTTPException(status_code=404, detail=f"No task found with id {task_id}")
    
    task_db_v1.remove(task)
    return {"status": "ok", "message": f"Task with id {task_id} has been deleted"}

@app.patch("/apiv1/tasks/{task_id}", status_code=200)
def modify_task_v1(task_id: int, task: Task):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid task ID. Must be greater than 0.")
    
    existing_task = get_task_by_id(task_id, task_db_v1)
    if not existing_task:
        raise HTTPException(status_code=404, detail=f"No task found with id {task_id}")
    
    existing_task["task_title"] = task.task_title
    existing_task["task_desc"] = task.task_desc
    existing_task["is_finished"] = task.is_finished
    
    return {"status": "updated", "task": existing_task}


# API Version 2 Endpoints
@app.get("/apiv2/tasks/{task_id}")
def fetch_task_v2(task_id: int, api_key: str = Depends(validate_api_key)):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid task ID. Must be greater than 0.")
    
    task = get_task_by_id(task_id, task_db_v2)
    if task is None:
        raise HTTPException(status_code=404, detail=f"No task found with id {task_id}")
    
    return {"status": "ok", "task": task}

@app.post("/apiv2/tasks", status_code=201)
def add_task_v2(task: Task, api_key: str = Depends(validate_api_key)):
    new_task_id = len(task_db_v2) + 1
    new_task = {
        "task_id": new_task_id,
        "task_title": task.task_title,
        "task_desc": task.task_desc,
        "is_finished": task.is_finished
    }
    task_db_v2.append(new_task)
    return {"status": "created", "task": new_task}

@app.patch("/apiv2/tasks/{task_id}", status_code=204)
def modify_task_v2(task_id: int, task: Task, api_key: str = Depends(validate_api_key)):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid task ID. Must be greater than 0.")
    
    existing_task = get_task_by_id(task_id, task_db_v2)
    if not existing_task:
        raise HTTPException(status_code=404, detail=f"No task found with id {task_id}")
    
    existing_task["task_title"] = task.task_title
    existing_task["task_desc"] = task.task_desc
    existing_task["is_finished"] = task.is_finished
    
    return {"status": "updated"}

@app.delete("/apiv2/tasks/{task_id}", status_code=204)
def remove_task_v2(task_id: int, api_key: str = Depends(validate_api_key)):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid task ID. Must be greater than 0.")
    
    task = get_task_by_id(task_id, task_db_v2)
    if not task:
        raise HTTPException(status_code=404, detail=f"No task found with id {task_id}")
    
    task_db_v2.remove(task)
    return {"status": "deleted"}
