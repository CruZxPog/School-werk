from flask import Flask
from flask import request
from flask import render_template
app = Flask(__name__)


cars = ["Toyota Supra", "BMW e30", "Mazda Miata", "Subaru WRX"]
introCarImgs= [
    #Supra
    "img/Supra/introSupra.jpg",
    #BMW E30
    "img/e30/introE30.jpg",
    #Miata
    "img/Miata/introMiata.jfif",
    #WRX
    "img/WRX/introWRX.jpg"
]
@app.route("/")
def home_page():
    return render_template("index.html", title="Home Page",CarList=cars, introCarImgs=introCarImgs)

supraImgs = [
    "img/Supra/img0.jpg",
    "img/Supra/img1.jpg",
    "img/Supra/img2.jpg",
    "img/Supra/img3.jpg",
    "img/Supra/img4.jpg",
    "img/Supra/img5.jpg",
    "img/Supra/img6.jpg",
    "img/Supra/img7.jpg",
]

creditsSupra = [
    'https://www.instagram.com/2jzluna/',
    'https://www.instagram.com/supra_m.k4/',
    'https://www.instagram.com/supra.page/',
    'https://www.instagram.com/suprahub/',
    'https://www.instagram.com/banira.supra/'
]
@app.route("/set0")
def supra_page():
    return render_template("set_page.html", title=cars[0], imgList=supraImgs, credits=creditsSupra,CarList=cars)

e30Imgs = [
    "img/e30/img0.jpg",
    "img/e30/img1.jpg",
    "img/e30/img2.jpg",
    "img/e30/img3.jpg",
    "img/e30/img4.jfif",
    "img/e30/img5.jpg",
    "img/e30/img6.jpg",
    "img/e30/img7.jpg",
]

creditsE30 = [
    'https://www.instagram.com/simp.e30/',
    'https://www.instagram.com/e30_jv/'
]

@app.route("/set1")
def e30_page():
    return render_template("set_page.html", title=cars[1], imgList=e30Imgs, credits=creditsE30,CarList=cars)

miataImgs = [
    "img/Miata/img0.jfif",
    "img/Miata/img1.jfif",
    "img/Miata/img2.jfif",
    "img/Miata/img3.jfif",
    "img/Miata/img4.jfif",
    "img/Miata/img5.jfif",
    "img/Miata/img6.jfif",
    "img/Miata/img7.jfif",
]

creditsMiata = [
    'https://www.instagram.com/miata.club/'
]
@app.route("/set2")
def miata_page():
    return render_template("set_page.html", title=cars[2], imgList=miataImgs, credits=creditsMiata,CarList=cars)

wrxImgs = [
    "img/WRX/img0.jpg",
    "img/WRX/img1.jpg",
    "img/WRX/img2.jpg",
    "img/WRX/img3.jpg",
    "img/WRX/img4.jpg",
    "img/WRX/img5.jpg",
    "img/WRX/img6.jpg",
    "img/WRX/img7.jpg",
]

creditsWRX = [
    'https://www.instagram.com/wrx_cult/'
]
@app.route("/set3")
def wrx_page():
    return render_template("set_page.html", title=cars[3], imgList=wrxImgs, credits=creditsWRX,CarList=cars)

app.run(host='0.0.0.0', port=6969)