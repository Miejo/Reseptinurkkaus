from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    sql = "SELECT COUNT(*) FROM recipes"
    result = db.session.execute(sql)
    count = result.fetchone()[0]
    return render_template("index.html", count=count)

@app.route("/recipes")
def recipes():
    sql = "SELECT id, name FROM recipes"
    result = db.session.execute(sql)
    recipes = result.fetchall()
    return render_template("recipes.html", recipes=recipes)

@app.route("/recipes/<int:id>")
def recipe(id):
    sql = "SELECT name FROM Recipes WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    title = result.fetchone()[0]
    sql = "SELECT name, quantity FROM Ingredients, RecipeIngredients WHERE Ingredients.id = ingredient_id AND recipe_id=:id"
    result = db.session.execute(sql, {"id":id})
    ingredients = result.fetchall()
    sql = "SELECT step, instructions FROM Steps WHERE recipe_id=:id"
    result = db.session.execute(sql, {"id":id})
    steps = result.fetchall()
    return render_template("recipe.html", name=title, ingredients=ingredients, steps=steps)

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    sql = "INSERT INTO Recipes (name) VALUES (:name) RETURNING id"
    result = db.session.execute(sql, {"name":name})
    recipe_id = result.fetchone()[0]
    ingredients = request.form.getlist("ingredient")
    quantities = request.form.getlist("quantity")
    steps = request.form.getlist("step")
    for index, ingredient in enumerate(ingredients):
        sql = "SELECT id FROM Ingredients WHERE name=:name"
        result = db.session.execute(sql, {"name":ingredient})
        if result.rowcount == 0:
            sql = "INSERT INTO Ingredients (name) VALUES (:name) RETURNING id"
            result = db.session.execute(sql, {"name":ingredient})
        ingredient_id = result.fetchone()[0]
        sql = "INSERT INTO RecipeIngredients (recipe_id, ingredient_id, quantity) VALUES (:recipe_id, :ingredient_id, :quantity)"
        db.session.execute(sql, {"recipe_id":recipe_id, "ingredient_id":ingredient_id, "quantity":quantities[index]})
    for index, step in enumerate(steps):
        sql = "INSERT INTO Steps (recipe_id, step, instructions) VALUES (:recipe_id, :step, :instruction)"
        order_number = index + 1
        db.session.execute(sql, {"recipe_id":recipe_id, "step":order_number, "instruction":step})
    db.session.commit()
    return redirect("/")