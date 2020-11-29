from db import db
import users

def get_rating(recipe_id):
    sql = "SELECT AVG(rating) FROM Ratings WHERE recipe_id=:recipe_id"
    result = db.session.execute(sql, {"recipe_id":recipe_id})
    rating = result.fetchone()[0]
    if rating == None:
        rating = -1
    rating = round(rating, 1)
    return rating

def rate(recipe_id, rating):
    username = users.get_user()
    if username is None:
        return False
    user_id = users.get_id()
    sql = "INSERT INTO Ratings(recipe_id, rating, user_id) VALUES (:recipe_id, :rating, :user_id)"
    db.session.execute(sql, {"recipe_id":recipe_id, "rating":rating, "user_id":user_id})
    db.session.commit()
    return True

def get_rating_status(recipe_id):
    username = users.get_user()
    if username is None:
        return True
    user_id = users.get_id()
    sql = "SELECT COUNT(*) FROM Ratings WHERE recipe_id=:recipe_id AND user_id=:user_id"
    result = db.session.execute(sql, {"recipe_id":recipe_id, "user_id":user_id})
    count = result.fetchone()[0]
    if count:
        return True
    return False