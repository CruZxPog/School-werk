from flask import Flask
from flask import render_template

app = Flask(__name__)

cars = ["Toyota Supra", "BMW e30", "Mazda Miata", "Subaru WRX"]
introCarImgs = [
    "img/Supra/introSupra.jpg",
    "img/e30/introE30.jpg",
    "img/Miata/introMiata.jfif",
    "img/WRX/introWRX.jpg"
]

images = [
    [
        "img/Supra/img0.jpg", "img/Supra/img1.jpg", "img/Supra/img2.jpg", "img/Supra/img3.jpg",
        "img/Supra/img4.jpg", "img/Supra/img5.jpg", "img/Supra/img6.jpg", "img/Supra/img7.jpg"
    ],
    [
        "img/e30/img0.jpg", "img/e30/img1.jpg", "img/e30/img2.jpg", "img/e30/img3.jpg",
        "img/e30/img4.jfif", "img/e30/img5.jpg", "img/e30/img6.jpg", "img/e30/img7.jpg"
    ],
    [
        "img/Miata/img0.jfif", "img/Miata/img1.jfif", "img/Miata/img2.jfif", "img/Miata/img3.jfif",
        "img/Miata/img4.jfif", "img/Miata/img5.jfif", "img/Miata/img6.jfif", "img/Miata/img7.jfif"
    ],
    [
        "img/WRX/img0.jpg", "img/WRX/img1.jpg", "img/WRX/img2.jpg", "img/WRX/img3.jpg",
        "img/WRX/img4.jpg", "img/WRX/img5.jpg", "img/WRX/img6.jpg", "img/WRX/img7.jpg"
    ]
]

credits = [
    [
        'https://www.instagram.com/2jzluna/', 'https://www.instagram.com/supra_m.k4/',
        'https://www.instagram.com/supra.page/', 'https://www.instagram.com/suprahub/',
        'https://www.instagram.com/banira.supra/'
    ],
    [
        'https://www.instagram.com/simp.e30/', 'https://www.instagram.com/e30_jv/'
    ],
    [
        'https://www.instagram.com/miata.club/'
    ],
    [
        'https://www.instagram.com/wrx_cult/'
    ]
]

@app.route("/")
def home_page():
    return render_template("index.html", title="Home Page", CarList=cars, introCarImgs=introCarImgs)

@app.route("/set/<int:carid>")
def car_page(carid):
    if 0 <= carid < len(cars):
        return render_template("set_page.html", title=cars[carid], imgList=images[carid], credits=credits[carid], CarList=cars)
    return "Car not found", 404

app.run(host='0.0.0.0', port=6969)

