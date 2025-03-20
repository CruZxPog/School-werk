from fastapi import FastAPI

app = FastAPI()

taken = [
    {"id": 1, "taak": "schoonmaken", "status":False},
    {"id": 2, "taak": "koken", "status": False},
    {"id": 3, "taak": "afwassen", "status": False}
]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/taken")
def read_todo():
    return  taken

@app.post("/taken")
def create_todo(taak: str):
    new_todo = {"taak": taak, "status": False}
    taken.append(new_todo)
    return new_todo

@app.delete("/taken/:id")
def delete_todo(id: int):
    taken = [todo for todo in taken if todo["id"] != id]
    return {"message": "Taak verwijderd"}