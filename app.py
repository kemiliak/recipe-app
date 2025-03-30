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
    options = [("Haku", "/search"), ("Lisää resepti", "/create"), \
               ("Omat reseptit", "/recipes"), ("Suosikit", "/page")]
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

@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    """
    Displays the selected recipe
    """
    recipe = recipes.get_recipe(recipe_id)
    instructions = [line.strip() for line in recipe[2].splitlines() if line.strip()]
    ingredients = [line.strip() for line in recipe[3].splitlines() if line.strip()]
    # TODO: comments = recipes.get_comments(recipe_id)
    return render_template("recipe.html", title=recipe[1], ingredients=ingredients, \
                           instructions=instructions, cooking_time=recipe[4], \
                            serving_size=recipe[5], created_at=recipe[6], creator=recipe[8])

@app.route("/create/", methods=["GET", "POST"])
def new_recipe():
    """
    Creates and displays a new recipe
    """
    if request.method == "GET":
        return render_template("create.html")
    if request.method == "POST":
        title = request.form["title"]
        instructions = request.form["instructions"]
        ingredients = request.form["ingredients"]
        cooking_time = request.form["cooking_time"]
        serving_size = request.form["serving_size"]
        user_id = session["user_id"]

        if not title or not ingredients or not instructions:
            # TODO: flash("Virhe: reseptin nimi, ainekset tai ohje puuttuu")
            return render_template("create.html")
        if len(title) > 35 or len(cooking_time) > 20 or len(serving_size) > 20:
            # TODO: flash("Virhe: nimi, aika tai annoskoko sisältää liikaa merkkejä")
            return render_template("create.html")
        if len(ingredients) > 5000 or len(instructions) > 5000:
            # TODO: flash("Virhe: ainekset tai ohjeet sisältää liikaa merkkejä")
            return render_template("create.html")

    recipe_id = recipes.add_recipe(title, instructions, ingredients, cooking_time, serving_size, user_id)
    return redirect("/recipe/" + str(recipe_id))

@app.route("/recipes")
def display_recipes():
    """Shows a list of recipes the user has created"""
    user_id = users.user_id()
    username = users.username(user_id)
    r = recipes.get_user_recipes(user_id)
    return render_template("recipes.html", recipes=r, user = username)

@app.route("/search", methods=["GET", "POST"])
def search():
    """
    Search feature that utilizes the display_recipes() function
    """
    if request.method == "GET":
        return render_template("search.html")
    if request.method == "POST":
        query = request.form.get("query")
        results = recipes.search(query) if query else recipes.get_recipes()
        return render_template("recipes.html", recipes=results, user="Kaikki")
