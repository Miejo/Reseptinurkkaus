from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            session["username"] = username
            return True
        else:
            return False
        
def logout():
    del session["username"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username,password)

def get_user():
    return session.get("username", None)

def get_id():
    username = get_user()
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    id = result.fetchone()[0]
    return id