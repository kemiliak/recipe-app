CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE recipes (
    recipe_id INTEGER PRIMARY KEY,
    title TEXT,
    instructions TEXT,
    ingredients TEXT,
    cooking_time TEXT,
    serving_size TEXT,
    created_at TEXT,
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE favorites (
    user_id INTEGER REFERENCES users(id),
    recipe_id INTEGER REFERENCES recipes(recipe_id),
    PRIMARY KEY (user_id, recipe_id)
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    comment TEXT,
    sent_at TEXT,
    user_id INTEGER REFERENCES users(id),
    recipe_id INTEGER REFERENCES recipes(recipe_id)
);