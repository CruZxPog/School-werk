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
    weight: float
    length: int
    barrel_length: int
    cartridge: str
    action: str
    muzzle_velocity: int
    effective_range: int
    magazine_capacity: int
    fire_rate: str
    img_url: str

gun_list = []
for gun_data in guns:
    #https://www.geeksforgeeks.org/python-unpack-dictionary/
    # ** is for unpacking the dictionary into keyword arguments
    gun_list.append(gun(**gun_data))

gun_categories = []
for gun in gun_list:
    if gun.category not in gun_categories:
        gun_categories.append(gun.category)

@app.route("/")
def start_page():
    return render_template("index.html",gun_categories=gun_categories,guns=gun_list)

@app.route("/category/<category>")
def category_page(category):
    guns_in_category = [gun for gun in gun_list if gun.category == category]
    return render_template("category.html",gun_categories=gun_categories, guns=guns_in_category, category=category)

@app.route("/category/<category>/gun/<int:gun_id>")
def gun_page(category,gun_id):
    gun = None
    for g in gun_list:
        if g.id == gun_id:
            gun = g
            break
    if gun:
        return render_template("gun.html", gun_categories=gun_categories, gun=gun)
    else:
        return "Gun not found", 404

if __name__ == '__main__':  
   app.run()