import db

def add_recipe(title, instructions, ingredients, cooking_time, serving_size, user_id):
    sql = """INSERT INTO recipes (title, instructions, ingredients, cooking_time, serving_size,
            created_at, user_id) VALUES (?, ?, ?, ?, ?, datetime('now'), ?)"""
    db.execute(sql, [title, instructions, ingredients, cooking_time, serving_size, user_id])
    recipe_id = db.last_insert_id()
    return recipe_id

def get_recipe(recipe_id):
    sql = """SELECT r.recipe_id, r.title, r.instructions, r.ingredients, r.cooking_time, 
             r.serving_size, r.created_at, r.user_id, u.username
             FROM recipes r, users u
             WHERE r.user_id = u.id AND recipe_id = ?"""
    return db.query(sql, [recipe_id])[0]

def get_user_recipes(user_id):
    sql = """SELECT recipe_id, title, instructions, ingredients, cooking_time, 
             serving_size, created_at, user_id
             FROM recipes
             WHERE user_id = ?"""
    return db.query(sql, [user_id])

def search(query):
    sql = """SELECT recipe_id, title, instructions, ingredients, cooking_time, 
             serving_size, created_at, user_id
             FROM recipes
             WHERE title LIKE ?
             ORDER BY created_at DESC"""
    return db.query(sql, ["%" + query + "%"])

def get_recipes():
    sql = """SELECT recipe_id, title, instructions, ingredients, cooking_time, 
             serving_size, created_at, user_id
             FROM recipes"""
    return db.query(sql)

def update_recipe(recipe_id, title, instructions, ingredients, cooking_time, serving_size, user_id):
    sql = """UPDATE recipes SET recipe_id = ?, title = ?, instructions = ?, ingredients = ?, 
             cooking_time = ?, serving_size = ?
             WHERE recipe_id = ? AND user_id = ?"""
    db.execute(sql, [recipe_id, title, instructions, ingredients, cooking_time, serving_size, recipe_id, user_id])

def creator_id(recipe_id):
    sql = "SELECT user_id FROM recipes WHERE recipe_id = ?"
    return db.query_one(sql, [recipe_id])[0]

def remove_recipe(recipe_id):
    sql = "DELETE FROM recipes WHERE recipe_id = ?"
    db.execute(sql, [recipe_id])

def add_favorites(user_id, recipe_id):
    sql = "INSERT INTO favorites (user_id, recipe_id) VALUES (?, ?)"
    db.execute(sql, [user_id, recipe_id])

def get_favorites(user_id):
    sql = """SELECT recipe_id, title, instructions, ingredients, cooking_time, 
             serving_size, created_at, user_id
             FROM recipes
             WHERE recipe_id IN (SELECT recipe_id FROM favorites WHERE user_id = ?)"""
    return db.query(sql, [user_id])

def get_favorites_ids(user_id):
    sql = "SELECT recipe_id FROM favorites WHERE user_id = ?"
    return [id[0] for id in db.query(sql, [user_id])]

def remove_favorite(recipe_id):
    sql = "DELETE FROM favorites WHERE recipe_id = ?"
    db.execute(sql, [recipe_id])
