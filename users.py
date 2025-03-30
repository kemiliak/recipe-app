from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import db

def register(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if len(result) == 1:
        user_id, password_hash = result[0]
        if check_password_hash(password_hash, password):
           return user_id
       
    return None

def user_id():
    return session.get("user_id", 0)

def username(id):
    result = db.query_one("SELECT username FROM users WHERE id = ?", (id,))
    if result:
        return result[0]
    return None