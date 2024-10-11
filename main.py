from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

task_db = [
    {"task_id": 1, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 2", "is_finished": False}
]

class Task(BaseModel):
    task_title: str = Field(..., min_length=1)
    task_desc: str = Field(..., min_length=1)
    is_finished: bool = False


def get_task_by_id(task_id: int):
    return next((task for task in task_db if task["task_id"] == task_id), None)

# GET 
@app.get("/tasks/{task_id}")
def fetch_task(task_id: int):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid task ID. Must be greater than 0.")
    
    task = get_task_by_id(task_id)
    if task is None:
        return {"error": f"No task found with id {task_id}"}
    
    return {"status": "ok", "task": task}

# POST 
@app.post("/tasks")
def add_task(task: Task):
    new_task_id = len(task_db) + 1
    new_task = {
        "task_id": new_task_id,
        "task_title": task.task_title,
        "task_desc": task.task_desc,
        "is_finished": task.is_finished
    }
    task_db.append(new_task)
    return {"status": "ok", "task": new_task}

# PATCH 
@app.patch("/tasks/{task_id}")
def modify_task(task_id: int, task: Task):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid task ID. Must be greater than 0.")
    
    existing_task = get_task_by_id(task_id)
    if not existing_task:
        return {"error": f"No task found with id {task_id}"}
    
    existing_task["task_title"] = task.task_title
    existing_task["task_desc"] = task.task_desc
    existing_task["is_finished"] = task.is_finished
    
    return {"status": "ok", "task": existing_task}

# DELETE 
@app.delete("/tasks/{task_id}")
def remove_task(task_id: int):
    if task_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid task ID. Must be greater than 0.")
    
    task = get_task_by_id(task_id)
    if not task:
        return {"error": f"No task found with id {task_id}"}
    
    task_db.remove(task)
    return {"status": "ok", "message": f"Task with id {task_id} has been deleted"}
