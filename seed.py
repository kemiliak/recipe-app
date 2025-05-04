import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM recipes")
db.execute("DELETE FROM favorites")

user_count = 1000
recipe_count = 10**5
comment_count = 10**6

for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, recipe_count + 1):
    db.execute("INSERT INTO recipes (title) VALUES (?)",
               ["recipe" + str(i)])

for i in range(1, comment_count + 1):
    user_id = random.randint(1, user_count)
    recipe_id = random.randint(1, comment_count)
    db.execute("""INSERT INTO comments (comment, sent_at, user_id, recipe_id)
                  VALUES (?, datetime('now'), ?, ?)""",
               ["comment" + str(i), user_id, recipe_id])

db.commit()
db.close()
