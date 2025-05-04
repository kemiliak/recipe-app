"""Module for application routes"""
import secrets, sqlite3
from flask import Flask
from flask import abort, flash, render_template, redirect, request, session, g
import users, recipes, config
import markupsafe
import time

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response

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
    Front page
    """
    require_login()
    user_id = session["user_id"]
    user = users.username(user_id)
    options = [("Haku", "/search"), ("Lisää resepti", "/create"), \
               ("Reseptit", "/recipes"), ("Oma profiili", "/profile"), ("Suosikit", "/favorites")]
    n_recipes = recipes.recipe_count()
    n_recipes = n_recipes if n_recipes else 0
    # best_recipe_id = recipes.most_popular_recipe()
    # best_recipe_id = best_recipe_id if best_recipe_id else False
    # recipe_title = recipes.get_recipe_name(best_recipe_id)

    return render_template("page.html", message="Tervetuloa", user=user, \
                           intro="Tällä sivulla voit luoda uusia reseptejä, tutkia omia sekä \
                            muiden reseptejä, käyttää hakuominaisuutta sekä tallentaa reseptejä suosikeiksi.", \
                            items=options, n_recipes=n_recipes)
    #                        best_recipe_id=best_recipe_id, recipe_title=recipe_title)

@app.route("/profile")
def user_profile_page():
    require_login()
    user_id = session["user_id"]
    username = users.username(user_id)
    users_recipes = recipes.get_user_recipes(user_id)
    users_recipe_count = recipes.users_recipe_count(user_id)
    users_recipe_count = users_recipe_count if users_recipe_count else 0
    return render_template("profile.html", recipes=users_recipes, user = username, users_recipe_count=users_recipe_count)

@app.route("/profile/<int:user_id>")
def show_user(user_id):
    require_login()
    user = users.username(user_id)
    if not user:
        abort(404)
    user_recipes = recipes.get_user_recipes(user_id)
    users_recipe_count = recipes.users_recipe_count(user_id)
    users_recipe_count = users_recipe_count if users_recipe_count else 0
    return render_template("profile.html", recipes=user_recipes, user=user, users_recipe_count=users_recipe_count)

@app.route("/login", methods=["GET","POST"])
def login():
    """
    Login
    """
    if request.method == "GET":
        return render_template("login.html", filled={})
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.login(username, password)

        if user_id:
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/page")
        else:
            flash("Virhe: Kirjautuminen epäonnistui! Väärä tunnus tai salasana")
            filled = {"username": username}
            return render_template("login.html", filled=filled)

@app.route("/logout")
def logout():
    """Logout"""
    require_login()
    del session["user_id"]
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    """Registration"""
    if request.method == "GET":
        return render_template("register.html", filled={})
    if request.method == "POST":
        username = request.form["username"]

        if not username or len(username) > 16:
            flash("Virhe: Epäsopiva käyttäjätunnus")
            filled = {"username": username}
            return render_template("register.html", filled=filled)
    
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if not password1:
            flash("Virhe: Salasana puuttuu!")
            filled = {"username": username}
            return render_template("register.html", filled=filled)
        if password1 != password2:
            flash("Virhe: Salasanat eroavat!")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

        try:
            users.register(username, password1)
            flash("Tunnuksen luonti onnistui")
            return redirect("/login")
        except sqlite3.IntegrityError:
            flash("Virhe: Tunnus on jo olemassa, kirjaudu sisään tai valitse uusi tunnus")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    """
    Displays the selected recipe
    """
    require_login()
    user_id = session["user_id"]
    recipes.visits(recipe_id)
    # only the creator can modify the original recipe
    user_is_creator = users.is_creator(recipes.creator_id(recipe_id))
    is_favorite = True if recipe_id in recipes.get_favorites_ids(user_id) else False
    recipe = recipes.get_recipe(recipe_id)

    instructions = [line.strip() for line in recipe[2].splitlines() if line.strip()]
    ingredients = [line.strip() for line in recipe[3].splitlines() if line.strip()]

    comments = recipes.get_comments(recipe_id)

    return render_template("recipe.html", title=recipe[1], ingredients=ingredients, \
                            instructions=instructions, cooking_time=recipe[4], \
                            serving_size=recipe[5], created_at=recipe[6], creator=recipe[8], \
                            user_is_creator=user_is_creator, is_favorite=is_favorite, \
                            recipe_id=recipe_id, comments=comments, user_id=recipe[7])

@app.route("/create/", methods=["GET", "POST"])
def new_recipe():
    """
    Creates and displays a new recipe
    """
    require_login()
    if request.method == "GET":
        return render_template("create.html", filled={})
    if request.method == "POST":
        check_csrf()
        title = request.form["title"]
        instructions = request.form["instructions"]
        ingredients = request.form["ingredients"]
        cooking_time = request.form["cooking_time"]
        serving_size = request.form["serving_size"]
        user_id = session["user_id"]

        filled = render_template("create.html", title=title, instructions=instructions, \
                                    ingredients=ingredients, cooking_time=cooking_time, \
                                    serving_size = serving_size)
        
        fields = [["nimi", title, 35], ["ainekset", ingredients, 5000], ["ohje", instructions, 5000],
                  ["valmistusaika", cooking_time, 35], ["annoskoko", serving_size, 35]]

        for field in fields[:3]:
            if not field[1]:
                flash(f"Virhe: Reseptin {field[0]} puuttuu")
                return filled
        for field in fields:
            if len(field[1]) > field[2]:
                flash(f"Virhe: Reseptin {field[0]} sisältää liikaa merkkejä")
                return filled

        recipe_id = recipes.add_recipe(title, instructions, ingredients, cooking_time, serving_size, user_id)
        return redirect("/recipe/" + str(recipe_id))

@app.route("/recipes")
def display_recipes():
    """Shows a list of recipes from all users"""
    require_login()
    r = recipes.get_recipes()
    return render_template("recipes.html", recipes=r, user="Kaikki")

@app.route("/search", methods=["GET", "POST"])
def search():
    """
    Search feature that utilizes the display_recipes() function
    """
    require_login()
    if request.method == "GET":
        return render_template("search.html")
    if request.method == "POST":
        check_csrf()
        query = request.form.get("query")
        results = recipes.search(query) if query else recipes.get_recipes()
        return render_template("recipes.html", recipes=results, user="Kaikki")

@app.route("/create/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = recipes.get_recipe(recipe_id)
    if request.method == "GET":
        return render_template("create.html", title=recipe[1], instructions=recipe[2], \
                                ingredients=recipe[3], cooking_time=recipe[4], serving_size=recipe[5], \
                                created_at=recipe[6], creator=recipe[8], recipe_id=recipe_id)
    if request.method == "POST":
        check_csrf()
        title = request.form["title"]
        instructions = request.form["instructions"]
        ingredients = request.form["ingredients"]
        cooking_time = request.form["cooking_time"]
        serving_size = request.form["serving_size"]
        user_id = session["user_id"]

        filled = render_template("create.html", title=title, instructions=instructions, \
                                ingredients=ingredients, cooking_time=cooking_time, serving_size=serving_size, \
                                created_at=recipe[6], creator=recipe[8], recipe_id=recipe_id)
        fields = [["nimi", title, 35], ["ainekset", ingredients, 5000], ["ohje", instructions, 5000],
                  ["valmistusaika", cooking_time, 35], ["annoskoko", serving_size, 35]]

        for field in fields[:3]:
            if not field[1]:
                flash(f"Virhe: Reseptin {field[0]} puuttuu")
                return filled
        for field in fields:
            if len(field[1]) > field[2]:
                flash(f"Virhe: Reseptin {field[0]} sisältää liikaa merkkejä")
                return filled

        recipes.update_recipe(recipe["recipe_id"], title, instructions, ingredients, cooking_time, serving_size, user_id)
        return redirect("/recipe/" + str(recipe["recipe_id"]))

@app.route("/remove/<int:recipe_id>", methods=["GET", "POST"])
def delete_recipe(recipe_id):
    require_login()

    recipe = recipes.get_recipe(recipe_id)
    user_id = session["user_id"]

    if not recipe or recipe["user_id"] != user_id:
        flash("Virhe: Reseptin poisto epäonnistui!")
        redirect("/recipe/" + str(recipe_id))

    if request.method == "GET":
        return render_template("remove.html", recipe=recipe, is_recipe=True)

    if request.method == "POST":
        check_csrf()
        if "continue" in request.form:
            recipes.remove_recipe(recipe["recipe_id"])

    return redirect("/profile")

@app.route("/add_to_favorites/<int:recipe_id>")
def add_to_favorites(recipe_id):
    require_login()
    # check that recipe is not already in favorites
    try:
        recipes.add_favorites(session["user_id"], recipe_id)
        return get_favorites()
    except sqlite3.IntegrityError:
        flash("VIRHE: resepti on jo suosikeissa")
        return show_recipe(recipe_id)

@app.route("/favorites", methods=["GET"])
def get_favorites():
    require_login()
    user_id = session["user_id"]
    res = recipes.get_favorites(user_id)
    if res:
        return render_template("recipes.html", recipes=res, user=users.username(user_id), favorites=True)
    else:
        return render_template("recipes.html", recipes="", user=users.username(user_id), favorites=True)
    
@app.route("/remove_favorite/<int:recipe_id>", methods=["POST", "GET"])
def remove_from_favorites(recipe_id):
    require_login()
    recipe = recipes.get_recipe(recipe_id)

    if request.method == "GET":
        return render_template("remove.html", recipe=recipe, is_recipe=False)

    if request.method == "POST":
        check_csrf()
        if "continue" in request.form:
            recipes.remove_favorite(recipe["recipe_id"])
            return redirect("/favorites")

@app.route("/comment/<int:recipe_id>", methods=["POST"])
def comment(recipe_id):
    require_login()
    check_csrf()

    comment = request.form["comment"]
    user_id = session["user_id"]

    if not comment:
        flash("VIRHE: Tyhjää kommenttia ei voi lähettää!")
        return redirect("/recipe/" + str(recipe_id))
    if len(comment) > 5000:
        flash("VIRHE: Kommentti on liian pitkä!")
        return redirect("/recipe/" + str(recipe_id))

    try:
        recipes.add_comment(comment, user_id, recipe_id)
        return show_recipe(recipe_id)
    except sqlite3.IntegrityError:
        flash("VIRHE: Kommentointi epäonnistui")
    
    return redirect("/recipe/" + str(recipe_id))

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)
