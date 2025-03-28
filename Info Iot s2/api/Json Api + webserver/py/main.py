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
from requests import get, post, put, delete
# https://pypi.org/project/requests/
app = Flask(__name__)

DATABASE_API_URL = "https://my-json-server.typicode.com/CruZxPog/json/guns"

@app.route("/")
def start_page():
    render_template("index.html")