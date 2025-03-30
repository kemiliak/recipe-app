"""Module for application routes"""
import sqlite3
from flask import Flask
from flask import flash, render_template, redirect, request, session
import users, recipes, config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    """
    Frontpage view 
    """
    options = ["Tallentaa ja poistaa omia reseptejä", "Hakea, kommentoida \
               ja lisätä suosikeiksi omia sekä muiden reseptejä"]
    return render_template("index.html", message="Tervetuloa!", \
                           intro="Tällä sovelluksella voit:", items=options,
                           reminder="Kirjauduthan sisään käyttääksesi toimintoja! :)")

@app.route("/page")
def home_page():
    """
    Personal page
    """
    user = users.username(users.user_id())
    options = [("Haku", "/page"), ("Lisää resepti", "/page"), \
               ("Omat reseptit", "/page"), ("Suosikit", "/page")]
    return render_template("page.html", message="Tervetuloa", user=user, \
                           intro="Tällä sivulla voit luoda uusia reseptejä, tutkia omia sekä \
                            tallentamiasi reseptejä sekä hakea reseptejä:", items=options)

@app.route("/login", methods=["GET","POST"])
def login():
    """
    Login
    """
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.login(username, password)

        if user_id:
            session["user_id"] = user_id
            return redirect("/page")
        else:
            flash("Virhe: Kirjautuminen epäonnistui! Väärä tunnus tai salasana")
            return render_template("login.html")

@app.route("/logout")
def logout():
    """Logout"""
    del session["user_id"]
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    """Registration"""
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            flash("Virhe: Salasanat eroavat!")
            return render_template("register.html")
        try:
            users.register(username, password1)
            flash("Tunnuksen luonti onnistui")
            return redirect("/login")
        except sqlite3.IntegrityError:
            flash("Virhe: Tunnus on jo olemassa, kirjaudu sisään tai valitse uusi tunnus")
            return render_template("register.html")
