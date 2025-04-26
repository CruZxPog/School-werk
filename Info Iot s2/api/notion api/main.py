import requests
import os
from dotenv import load_dotenv


# Laad de environment-variabelen
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")


headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def fetch_database():
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
            print(f"- {name}: {status}, Location: {location}, Metadata: {metadata}, id: {id}")
    else:
        print(f"Fout: {response.status_code}")

fetch_database()

def add_task(name, status, priority):
    url = "https://api.notion.com/v1/pages"
   
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": name}}]},
            "Status": {"status": {"name": status}},
            "Priority": {"select": {"name": priority}},
        },
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"Taak '{name}' toegevoegd!")
    else:
        print(f"Fout: {response.status_code} - {response.text}")

#add_task("Dit is een nieuwe taak", "Done", "Medium")

def update_task(task_id, new_status=None, new_priority=None, new_name=None):
    url = f"https://api.notion.com/v1/pages/{task_id}"
    
    # Bouw de payload op basis van de opgegeven parameters
    properties = {}

    if new_name:
        properties["Name"] = {
            "title": [{"text": {"content": new_name}}]
        }

    if new_status:
        properties["Status"] = {
            "status": {"name": new_status}
        }

    if new_priority:
        properties["Priority"] = {
            "select": {"name": new_priority}
        }
    
    payload = {"properties": properties}
    
    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"Taak met ID '{task_id}' succesvol bijgewerkt!")
    else:
        print(f"Fout bij bijwerken: {response.status_code}, {response.text}")

# Voorbeeld: Update een taak
#task_id = update_task(
#     task_id="1de9bb6f-827b-810a-a114-e7a70082ea50", # verplicht veld
#     new_status="Done",
#     new_priority="Low",
#     new_name="Nieuwe naam voor de taak",
# ) 