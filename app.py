from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    """
    Frontpage view 
    """
    options = ["Tallentaa ja poistaa omia reseptejä", "Hakea, kommentoida ja lisätä suosikeiksi omia sekä muiden reseptejä", ]
    return render_template("index.html", message="Tervetuloa!", intro="Tällä sovelluksella voit:", items=options, 
                           reminder="Kirjauduthan sisään käyttääksesi toimintoja! :)")

@app.route("/page")
def home_page():
    """
    Personal page
    """
    options = [("Haku", ""), ("Lisää resepti", ""), ("Omat reseptit", ""), ("Suosikit", "")]
    return render_template("page.html", message="Tervetuloa", user="Testi", \
                           intro="Tällä sivulla voit luoda uusia reseptejä, tutkia omia sekä \
                            tallentamiasi reseptejä sekä hakea reseptejä:", items=options)