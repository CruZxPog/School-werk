#             █████████                  █████                    
#             ███░░░░░███                ░░███                    
#            ░███    ░███  ████████    ███████  ████████   ██████ 
#            ░███████████ ░░███░░███  ███░░███ ░░███░░███ ███░░███
#            ░███░░░░░███  ░███ ░███ ░███ ░███  ░███ ░░░ ░███████ 
#            ░███    ░███  ░███ ░███ ░███ ░███  ░███     ░███░░░  
#            █████   █████ ████ █████░░████████ █████    ░░██████ 
#            ░░░░░   ░░░░░ ░░░░ ░░░░░  ░░░░░░░░ ░░░░░      ░░░░░░ 

# Vergeet de bronnen niet toe te voegen!
# Bronnen:
# chatgpt.com (28/03)
# copilot.github.com (28/03)


from flask import Flask
from flask import render_template
import requests
from pydantic import BaseModel
# https://pypi.org/project/requests/

app = Flask(__name__)

DATABASE_API_URL = "https://my-json-server.typicode.com/CruZxPog/json/guns"

response = requests.get(DATABASE_API_URL)
guns = response.json()

class gun(BaseModel):
    id: int
    name: str
    category: str
    weight: str
    length: str
    barrel_length: str
    cartridge: str
    action: str
    muzzle_velocity: str
    effective_range: str
    magazine_capacity: str
    fire_rate: str
    img_url: str

gun_list = []
for gun_data in guns:
    #https://www.geeksforgeeks.org/python-unpack-dictionary/
    # ** is for unpacking the dictionary into keyword arguments
    gun_list.append(gun(**gun_data))

#print(gun_list)


@app.route("/")
def start_page():
    gun_types = [gun.category for gun in gun_list]
    render_template("index.html",guns=gun_types)