import sqlite3
import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    user = db.query_one("SELECT id, password FROM users WHERE username = ?", (username,))
    
    if not user:
        return False
    else:
        user_id, hashed_password = user
        if check_password_hash(hashed_password, password):
            session["user_id"] = user_id
            return True
        else:
            return False

def logout():
    session.pop("user_id", None)

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_value))
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
        return False
    return login(username, password)

def user_id():
    return session.get("user_id", 0)

def username(id):
    try:
        result = db.query_one("SELECT username FROM users WHERE id = ?", (id,))
        if result:
            return result[0]
    except sqlite3.Error as e:
        print(f"Error: {e}")
    return None