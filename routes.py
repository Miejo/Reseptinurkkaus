from app import app
from flask import render_template, request, redirect, flash
import users, recipes, ratings

@app.route("/")
def index():
    count = recipes.get_count()
    return render_template("index.html", count=count)

@app.route("/recipelist")
def recipelist():
    recipelist = recipes.get_list()
    return render_template("recipelist.html", recipelist=recipelist)

@app.route("/search")
def search():
    query = request.args["query"]
    recipelist = recipes.query_recipes(query)
    return render_template("recipelist.html", recipelist=recipelist)

@app.route("/recipelist/<int:id>", methods=["GET", "POST"])
def recipe(id):
    if request.method == "POST":
        rate = request.form["rate"]
        ratings.rate(id, rate)
    name, ingredients, steps, image = recipes.get_recipe(id)
    rating = ratings.get_rating(id)
    rating_status = ratings.get_rating_status(id)
    return render_template("recipe.html", id=id, name=name, rating=rating, ingredients=ingredients, steps=steps, image=image, rating_status=rating_status)

@app.route("/new", methods=["GET", "POST"])
def new():
    ingredients = 3
    steps = 3
    if request.method == "POST":
        ingredients = int(request.form["ingredient_rows"])
        steps = int(request.form["step_rows"])
        if request.form.get("add_ingredient", False):
            ingredients += 1
        elif request.form.get("remove_ingredient", False):
            if ingredients > 1:
                ingredients -= 1
        elif request.form.get("add_step", False):
            steps += 1
        elif request.form.get("remove_step", False):
            if steps > 1:
                steps -= 1
    return render_template("new.html", ingredients=ingredients, steps=steps)

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    ingredients = request.form.getlist("ingredient")
    quantities = request.form.getlist("quantity")
    steps = request.form.getlist("step")
    if request.files["image"].filename is not '':
        image = request.files["image"]
        print("name",image.filename)
    else:
        image = None
    if recipes.add_recipe(name, ingredients, quantities, steps, image):
        return redirect("/")
    else:
        pass


@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        error = None
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            error = "Väärä käyttäjätunnus tai salasana"
            return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username, password):
            return redirect("/")
        else:
            error = "Rekisteröinti epäonnistui"
            return render_template("register.html", error=error)