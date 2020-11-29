from db import db
import users

def get_count():
    sql = "SELECT COUNT(*) FROM recipes"
    result = db.session.execute(sql)
    count = result.fetchone()[0]
    return count

def get_list():
    sql = "SELECT id, name FROM recipes"
    result = db.session.execute(sql)
    recipes = result.fetchall()
    return recipes

def get_recipe(id):
    sql = "SELECT name FROM Recipes WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    name = result.fetchone()[0]
    sql = "SELECT name, quantity FROM Ingredients, RecipeIngredients WHERE Ingredients.id = ingredient_id AND recipe_id=:id"
    result = db.session.execute(sql, {"id":id})
    ingredients = result.fetchall()
    sql = "SELECT step, instructions FROM Steps WHERE recipe_id=:id"
    result = db.session.execute(sql, {"id":id})
    steps = result.fetchall()
    return name, ingredients, steps

def add_recipe(name, ingredients, quantities, steps):
    username = users.get_user()
    if username is None:
        return False
    sql = "INSERT INTO Recipes (name) VALUES (:name) RETURNING id"
    result = db.session.execute(sql, {"name":name})
    recipe_id = result.fetchone()[0]
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
    return True