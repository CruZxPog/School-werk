from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union


app = FastAPI()

id_counter = 1

tasks = []

class Task(BaseModel):
    id: int
    task: str
    status: Union[bool, None] = False

@app.get("/tasks")
def read_todo():
    return tasks

@app.post("/tasks/{task}")
def create_new_task(task_new: str, status: Union[bool, None]=False):
    global id_counter 
    new_task = Task(id=id_counter, task=task_new, status=status)
    id_counter += 1
    tasks.append(new_task)
    return new_task

@app.put("/completeTask/{task_id}")
def update_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            task.status = True
            return task
    return {"message": "Task not found"}

@app.delete("/deleteTask/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    return {"message": "Task not found"}