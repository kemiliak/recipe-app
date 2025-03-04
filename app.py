import users, db, config
from flask import Flask
from flask import render_template,  redirect, request

app = Flask(__name__)
app.secret_key = config.secret_key

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
    options = [("Haku", "/page"), ("Lisää resepti", "/page"), ("Omat reseptit", "/page"), ("Suosikit", "/page")]
    return render_template("page.html", message="Tervetuloa", user="Testi", \
                           intro="Tällä sivulla voit luoda uusia reseptejä, tutkia omia sekä \
                            tallentamiasi reseptejä sekä hakea reseptejä:", items=options)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return home_page()
        else:
            return render_template("error.html", message="Kirjautuminen epäonnistui!")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat!")
        if users.register(username, password1):
            return redirect("/login")
        else:
            return render_template("error.html", message="Tunnuksen luonti epäonnistui!")