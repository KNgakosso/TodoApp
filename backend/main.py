from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os
import uvicorn

import backend.task_service as ts
from backend.models import TaskModel, TaskListModel

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend/
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")   # ../frontend par rapport à backend/

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/', response_class=HTMLResponse)
def read_root():
    # Sert le frontend/index.html
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("<h1>Frontend not found</h1>", status_code=404)

@app.post('/tasks')
def create_task_endpoint(task_model : TaskModel, list_name : str | None = None):
    task = ts.create_task(task_model, list_name)
    return task

@app.get("/tasks")
def read_tasks_endpoint():
    return ts.get_tasks()

@app.get('/tasks/{task_id}')
def read_a_task_endpoint(task_id : int):
    try:
        return ts.get_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.patch("/tasks/{task_id}")
def toggle_task_endpoint(task_id : int):
    try:
        return ts.toggle_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete('/tasks/{task_id}')
def delete_task_endpoint(task_id : int):
    try:
        return ts.delete_task(task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post('/lists')
def create_task_list_endpoint(task_list_model : TaskListModel):
    task_list = ts.create_task_list(task_list_model)
    return task_list

@app.get("/lists")
def read_task_lists_endpoint():
    return ts.get_task_lists()

@app.get("/lists/{task_list_name}")
def read_a_task_list_endpoint(task_list_name : str):
    try:
        return ts.get_task_list(task_list_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@app.delete('/tasks/{task_list_name}')
def delete_task_list_endpoint(task_list_name : str):
    try:
        return ts.delete_task_list(task_list_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@app.get("/tasks/status/ongoing")
def read_ongoing_tasks_endpoint():
    return ts.get_ongoing_tasks()

@app.get("/tasks/status/completed")
def read_completed_tasks_endpoint():
    return ts.get_completed_tasks()

@app.put("/tasks/{task_id}")
def update_task_endpoint(task_id : int, task_model : TaskModel):
    try:
        return ts.update_task(task_id, task_model)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
@app.post('/lists/{list_name}/task')
def create_task_from_list_endpoint(list_name : str, task_model : TaskModel):
    try:
        task = ts.create_task(task_model, list_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return task
"""



@app.patch("/tasks/task_{task_id}/list")
def transfer_to_other_list(task_id : int, list_name : str | None = None):
    previous_list = tasks_dict[task_id].list_name
    if previous_list :
        lists_tasks[previous_list].remove(task_id)
    if list_name:
        lists_tasks[list_name].add(task_id)
    tasks_dict[task_id].list_name = list_name
    return tasks_dict[task_id]

    """