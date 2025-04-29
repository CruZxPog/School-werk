#             █████████                  █████                    
#             ███░░░░░███                ░░███                    
#            ░███    ░███  ████████    ███████  ████████   ██████ 
#            ░███████████ ░░███░░███  ███░░███ ░░███░░███ ███░░███
#            ░███░░░░░███  ░███ ░███ ░███ ░███  ░███ ░░░ ░███████ 
#            ░███    ░███  ░███ ░███ ░███ ░███  ░███     ░███░░░  
#            █████   █████ ████ █████░░████████ █████    ░░██████ 
#            ░░░░░   ░░░░░ ░░░░ ░░░░░  ░░░░░░░░ ░░░░░      ░░░░░░ 


# Bronnen:
# chatgpt.com (28/03)
# copilot.github.com (28/03)
# https://pypi.org/project/requests/ (28/03)
#https://www.geeksforgeeks.org/python-unpack-dictionary/ (28/03)


from flask import Flask
from flask import render_template
import requests
# https://pypi.org/project/requests/ (28/03)

app = Flask(__name__)

GUNS_DATABASE_API_URL = "https://my-json-server.typicode.com/CruZxPog/json/guns"
CATEGORIES_DATABASE_API_URL = "https://my-json-server.typicode.com/cruZxPog/json/categories"

guns_response = requests.get(GUNS_DATABASE_API_URL)
categories_response = requests.get(CATEGORIES_DATABASE_API_URL)

guns = guns_response.json()
categories = categories_response.json()

category_map = {cat["id"]: cat["naam"] for cat in categories}

for gun in guns:
    gun["category_name"] = category_map.get(gun["category_id"], "Onbekend")

gun_categories = list(category_map.values())

@app.route("/")
def start_page():
    return render_template("index.html", gun_categories=gun_categories, guns=guns)

@app.route("/category/<category>")
def category_page(category):
    guns_in_category = [gun for gun in guns if gun["category_name"] == category]
    return render_template("category.html", gun_categories=gun_categories, guns=guns_in_category, category=category)

@app.route("/category/<category>/gun/<int:gun_id>")
def gun_page(category, gun_id):
    gun = next((g for g in guns if g["id"] == gun_id), None)
    if gun:
        return render_template("gun.html", gun_categories=gun_categories, gun=gun)
    else:
        return "Gun not found", 404


#zonder dit werkte de app niet
#gekregen van chatgpt als mogelijk oplosing (28/03)
if __name__ == '__main__':  
   app.run()