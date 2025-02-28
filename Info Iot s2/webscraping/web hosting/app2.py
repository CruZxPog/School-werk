from flask import Flask, render_template
import random


app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("index.html", title="Home Page", name="Student")

@app.route("/users")
def users_page():
    user_list = ["bob","boby","lobby","jobby"]
    return render_template("users.html",users=user_list)

@app.route("/status")
def status():
    user_logged_in = True
    return render_template("status.html", logged_in=user_logged_in)


quote_list = [
    '“a“ - Gawr Gura'
    '“watah in the fire why?“ - Korone'
    '“Do you guys like get colds when uh, when it’s freezing?“ - xqc'
]

@app.route("/quote")
def quote_page():
    quote = random.choice(quote_list)
    return render_template("quotes.html", quote=quote)


app.run(host="0.0.0.0",port=6969)