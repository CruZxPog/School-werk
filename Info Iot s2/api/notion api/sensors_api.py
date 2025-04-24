#		     █████████                  █████                    
#			 ███░░░░░███                ░░███                    
#			░███    ░███  ████████    ███████  ████████   ██████ 
#			░███████████ ░░███░░███  ███░░███ ░░███░░███ ███░░███
#			░███░░░░░███  ░███ ░███ ░███ ░███  ░███ ░░░ ░███████ 
#			░███    ░███  ░███ ░███ ░███ ░███  ░███     ░███░░░  
#			█████   █████ ████ █████░░████████ █████    ░░██████ 
#			░░░░░   ░░░░░ ░░░░ ░░░░░  ░░░░░░░░ ░░░░░      ░░░░░░ 

# Vergeet de bronnen niet toe te voegen!
# Bronnen:
# chatgpt.com (24/04)
# copilot.github.com (24/04)
# https://developers.notion.com/reference/delete-a-block (24/04)
# https://core.telegram.org/api (24/04) 
# https://core.telegram.org/bots (24/04)

from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
# BaseModel is used to define a structured data model for sensors, ensuring validation and serialization. 
# This approach is preferred over using plain dictionaries or manual validation because it provides built-in type checking
# https://docs.pydantic.dev/latest/api/base_model/

# Laad de environment-variabelen
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")
BOTTOKEN = os.getenv("BOTTOKEN")
USERID = os.getenv("USERID")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

app = FastAPI()



class Sensor(BaseModel):
    name: str
    location: str
    status: str = "inactive"
    metadata: str = None
    id: str

sensors = []

def get_sensors():
    sensors.clear()
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print(response.json())
        data = response.json()
        print("Taken in de database:")
        for result in data["results"]:
            name = result["properties"]["Name"]["title"][0]["text"]["content"]
            location = result["properties"]["Location"]["rich_text"][0]["text"]["content"]
            status = result["properties"]["Status"]["select"]["name"]
            metadata = result["properties"]["Metadata"]["rich_text"][0]["text"]["content"]
            id = result["id"]
            sensor = Sensor(name=name, location=location, status=status, metadata=metadata, id=id)
            sensors.append(sensor)
    else:
        sensors.append(f"Fout: {response.status_code} - {response.text}")

# get requests
@app.get("/sensors")
def list_sensors():
    get_sensors()
    return sensors

def get_sensors_by_id(sensor_id: str):
    url = f"https://api.notion.com/v1/pages/{sensor_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        name = data["properties"]["Name"]["title"][0]["text"]["content"]
        location = data["properties"]["Location"]["rich_text"][0]["text"]["content"]
        status = data["properties"]["Status"]["select"]["name"]
        metadata = data["properties"]["Metadata"]["rich_text"][0]["text"]["content"]
        sensor = Sensor(name=name, location=location, status=status, metadata=metadata, id=sensor_id)
        return sensor
    else:
        return {"message": f"Fout: {response.status_code} - {response.text}"}

@app.get("/sensors/{sensor_id}")
def list_sensor(sensor_id: str):
    return get_sensors_by_id(sensor_id)


@app.post("/sensors")
def create_new_sensors(name: str, location: str, status: str = "Inactive", metadata: str = ""):
    url = "https://api.notion.com/v1/pages"
   
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": name}}]},
            "Location": {"rich_text": [{"text": {"content": location}}]},
            "Status": {"select": {"name": status}},
            "Metadata": {"rich_text": [{"text": {"content": metadata}}]},
        },
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code in [200, 201]:
        message = f"Sensor '{name}' toegevoegd!"
        url = (
            "https://api.telegram.org/bot"
            + BOTTOKEN
            + "/sendMessage?chat_id="
            + USERID
            + "&text="
            + message
        )
        requests.get(url).json()
        return  message
    else:
       return  {"message": f"Fout: {response.status_code} - {response.text}"} 
    

# # put requests
@app.patch("/sensors/{sensor_id}")
def update_sensor(sensor_id: str, new_name: str = None, new_location: str = None, new_status: str = "Inactive", new_metadata: str = None):
    url = f"https://api.notion.com/v1/pages/{sensor_id}"
    old_sensor_data = get_sensors_by_id(sensor_id)
    for sensor in sensors:
        if sensor.id == sensor_id:
            old_sensor_data = sensor
            break
    properties = {}

    if new_name:
        properties["Name"] = {
            "title": [{"text": {"content": new_name}}]
        }

    if new_location:
        properties["Location"] = {
            "rich_text": [{"text": {"content": new_location}}]
        }

    if new_status:
        properties["Status"] = {
            "select": {"name": new_status}
        }

    if new_metadata:
        properties["Metadata"] = {
            "rich_text": [{"text": {"content": new_metadata}}]
        }
    
    payload = {"properties": properties}
    
    response = requests.patch(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        message = (
            f"Sensor met ID '{sensor_id}' succesvol bijgewerkt!\n"
            f"Naam: '{old_sensor_data.name}' → '{new_name}'\n"
            f"Locatie: '{old_sensor_data.location}' → '{new_location}'\n"
            f"Status: '{old_sensor_data.status}' → '{new_status}'\n"
            f"Metadata: '{old_sensor_data.metadata}' → '{new_metadata}'"
        )

        url = (
            "https://api.telegram.org/bot"
            + BOTTOKEN
            + "/sendMessage?chat_id="
            + USERID
            + "&text="
            + message
        )
        requests.get(url).json()
        return  message
    else:
        return {"message": f"Fout bij bijwerken: {response.status_code}, {response.text}"}

@app.delete("/sensors/{sensor_id}")
def delete_sensor(sensor_id: str):
    deleted_sensor = get_sensors_by_id(sensor_id)
  
    url = f"https://api.notion.com/v1/blocks/{sensor_id}"
    
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 200:
        message = (
            f"Sensor met ID '{sensor_id}' succesvol verwijdert!\n"
            f"Naam: '{deleted_sensor.name}'\n"
            f"Locatie: '{deleted_sensor.location}'\n"
            f"Status: '{deleted_sensor.status}'\n"
            f"Metadata: '{deleted_sensor.metadata}'"
        )
        url = (
            "https://api.telegram.org/bot"
            + BOTTOKEN
            + "/sendMessage?chat_id="
            + USERID
            + "&text="
            + message
        )
        requests.get(url).json()
        return  message
    else:
        return {"message": f"Fout bij verwijderen: {response.status_code}, {response.text}"}