from fastapi import FastAPI
from pydantic import BaseModel
# BaseModel is used to define a structured data model for sensors, ensuring validation and serialization. 
# This approach is preferred over using plain dictionaries or manual validation because it provides built-in type checking
# https://docs.pydantic.dev/latest/api/base_model/

app = FastAPI()

id_counter = 1

sensors = []

class Sensor(BaseModel):
    id: int
    name: str
    location: str
    status: bool = False

# get requests

@app.get("/sensors")
def list_sensors():
    return sensors

@app.get("/sensors/{sensor_id}")
def list_sensor(sensor_id: int):
    for sensor in sensors:
        if sensor.id == sensor_id:
            return sensor
    return {"message": "sensor not found"}

@app.get("/sensors/status/{status}")
def list_sensor_status(status: bool):
    for sensor in sensors:
        if sensor.status == status:
            return sensor
    return {"message": f"no sensor with status: {str(status)} found"}

# post requests

@app.post("/sensors/{sensor}")
def create_new_sensors(name: str, location: str, status: bool=False ):
    global id_counter 
    new_sensor = Sensor(id=id_counter, name=name, location= location, status=status)
    id_counter += 1
    sensors.append(new_sensor)
    return new_sensor

# put requests

@app.put("/sensors/activate/{sensor_id}")
def activate_sensor(sensor_id: int):
    for sensor in sensors:
        if sensor.id == sensor_id:
            sensor.status = True
            return sensor
    return {"message": "sensor not found"}

@app.put("/sensors/deactivate/{sensor_id}")
def deactivate_sensor(sensor_id: int):
    for sensor in sensors:
        if sensor.id == sensor_id:
            sensor.status = False
            return sensor
    return {"message": "sensor not found"}

@app.put("/sensors/update/{sensor_id}")
def update_sensor(sensor_id: int, name: str, location: str):
    for sensor in sensors:
        if sensor.id == sensor_id:
            sensor.name = name
            sensor.location = location
            return sensor
    return {"message": "sensor not found"}
# delete requests

@app.delete("/sensors/{sensor_id}")
def delete_sensor(sensor_id: int):
    for sensor in sensors:
        if sensor.id == sensor_id:
            sensors.remove(sensor)
            return {"message": "sensor deleted"}
    return {"message": "sensor not found"}