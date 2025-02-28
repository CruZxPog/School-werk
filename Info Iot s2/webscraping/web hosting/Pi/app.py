from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask on Raspberry Pi from laptop!"


app.run(host='0.0.0.0', port=5000)