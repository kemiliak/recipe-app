CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE recipes (
    recipe_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    instructions TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    cooking_time TEXT,
    serving_size TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL REFERENCES users(id),
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE favorites (
    user_id INTEGER NOT NULL REFERENCES users(id),
    recipe_id INTEGER NOT NULL REFERENCES recipes(recipe_id),
    PRIMARY KEY (user_id, recipe_id)
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    comment TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL REFERENCES users(id),
    recipe_id INTEGER NOT NULL REFERENCES recipes(recipe_id)
);