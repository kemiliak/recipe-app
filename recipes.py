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
