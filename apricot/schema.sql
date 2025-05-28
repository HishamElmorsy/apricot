-- users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL
);

-- wishlist table
CREATE TABLE IF NOT EXISTS wishlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    game_title TEXT NOT NULL,
    cheapshark_game_id TEXT NOT NULL,
    UNIQUE(user_id, cheapshark_game_id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);
