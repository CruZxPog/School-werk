from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def start_page():
    return '<h1 style="display: flex; justify-content: center; align-items: center; height: 100vh;">Try /meow !!! :3</h1>'

@app.route("/meow")
def meow():
    return '<img src="C:\Code\HTML\img\icon.jpg" alt="cat" width="600" height="600">'

@app.route("/user/<name>")
def greet_user(name):
    return f"Hello, {name}!"

@app.route("/plus/<string:num1>/<string:num2>")
def plus(num1, num2):
    number1 = int(num1)
    number2 = int(num2) 
    return f"{number1} + {number2} = {number1+number2}"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        adminUsername = "admin"
        adminPassword = "admin"

        if username == adminUsername and password == adminPassword:
            return f"Hello, {username}!"
        
        return "Wrong password or username!"


    else:
        return '''
            <form method="post">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password">
                <input type="submit" value="Submit">
            </form>
        '''

artikelen = [
    {
        "id": 0,
        "titel": "Eerste Blogartikel",
        "inhoud": "Dit is de inhoud van het eerste blogartikel. Hier schrijf je over interessante onderwerpen die je wilt delen met je lezers.",
    },
    {
        "id": 1,
        "titel": "Tweede Blogartikel",
        "inhoud": "Dit is het tweede artikel. Je kunt hier verder ingaan op andere onderwerpen of voortborduren op het eerste artikel.",
    },
    {
        "id": 2,
        "titel": "Derde Blogartikel",
        "inhoud": "Het derde artikel kan bijvoorbeeld gaan over je ervaringen met het leren van Flask en het bouwen van webapplicaties.",
    },
]

@app.route("/blog")
def blog_start():
    buttons_html = ""
    for artikel in artikelen:
        buttons_html += f'''
            <button><a href="/blog/{artikel["id"]}">{artikel["titel"]}</a></button>
        '''
    return buttons_html

@app.route("/blog/<int:id>)")
def blog_page(id):
    artikel = artikelen[id]
    return f'<h1>{artikel["titel"]}</h1><p>{artikel["inhoud"]}</p>'


app.run(host="0.0.0.0", port=6969)