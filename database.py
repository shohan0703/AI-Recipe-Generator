import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Optional

from config import DB_PATH


class Database:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = str(db_path)
        self.initialize()

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def initialize(self):
        with self.connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    preferred_cuisine TEXT DEFAULT 'Any',
                    dietary_preference TEXT DEFAULT 'None'
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS recipes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    recipe_name TEXT NOT NULL,
                    description TEXT,
                    ingredients TEXT NOT NULL,
                    instructions TEXT NOT NULL,
                    cuisine TEXT,
                    meal_type TEXT,
                    dietary_preference TEXT,
                    difficulty TEXT,
                    prep_time TEXT,
                    cook_time TEXT,
                    total_time TEXT,
                    servings INTEGER,
                    calories INTEGER,
                    protein REAL,
                    carbs REAL,
                    fat REAL,
                    cooking_tips TEXT,
                    image_path TEXT,
                    created_at TEXT NOT NULL,
                    is_saved INTEGER DEFAULT 0,
                    is_favorite INTEGER DEFAULT 0,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_recipes_user ON recipes(user_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_recipes_created ON recipes(created_at)")

    def create_user(self, name, email, password_hash):
        with self.connect() as conn:
            cur = conn.execute(
                "INSERT INTO users(name,email,password) VALUES(?,?,?)",
                (name, email.lower().strip(), password_hash),
            )
            return cur.lastrowid

    def get_user_by_email(self, email):
        with self.connect() as conn:
            return conn.execute("SELECT * FROM users WHERE email=?", (email.lower().strip(),)).fetchone()

    def get_user(self, user_id):
        with self.connect() as conn:
            return conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()

    def update_user(self, user_id, name, preferred_cuisine, dietary_preference):
        with self.connect() as conn:
            conn.execute(
                "UPDATE users SET name=?, preferred_cuisine=?, dietary_preference=? WHERE id=?",
                (name, preferred_cuisine, dietary_preference, user_id),
            )

    def reset_password(self, email, password_hash):
        with self.connect() as conn:
            cur = conn.execute("UPDATE users SET password=? WHERE email=?", (password_hash, email.lower().strip()))
            return cur.rowcount > 0

    def add_recipe(self, user_id, data, image_path=""):
        with self.connect() as conn:
            cur = conn.execute("""
                INSERT INTO recipes(
                    user_id, recipe_name, description, ingredients, instructions,
                    cuisine, meal_type, dietary_preference, difficulty,
                    prep_time, cook_time, total_time, servings, calories,
                    protein, carbs, fat, cooking_tips, image_path, created_at
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                user_id, data["recipe_name"], data.get("description", ""),
                data.get("ingredients", []).__class__.__name__ and __import__("json").dumps(data.get("ingredients", [])),
                __import__("json").dumps(data.get("instructions", [])),
                data.get("cuisine", "Any"), data.get("meal_type", ""),
                data.get("dietary_preference", "None"), data.get("difficulty", "Easy"),
                data.get("prep_time", ""), data.get("cook_time", ""), data.get("total_time", ""),
                int(data.get("servings", 1)), int(data.get("calories", 0) or 0),
                float(data.get("protein", 0) or 0), float(data.get("carbs", 0) or 0), float(data.get("fat", 0) or 0),
                __import__("json").dumps(data.get("cooking_tips", [])), image_path,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            return cur.lastrowid

    def get_recipe(self, recipe_id, user_id):
        with self.connect() as conn:
            return conn.execute("SELECT * FROM recipes WHERE id=? AND user_id=?", (recipe_id, user_id)).fetchone()

    def list_recipes(self, user_id, saved_only=False, favorites_only=False, search=""):
        query = "SELECT * FROM recipes WHERE user_id=?"
        params = [user_id]
        if saved_only:
            query += " AND is_saved=1"
        if favorites_only:
            query += " AND is_favorite=1"
        if search:
            query += " AND recipe_name LIKE ?"
            params.append(f"%{search}%")
        query += " ORDER BY datetime(created_at) DESC"
        with self.connect() as conn:
            return conn.execute(query, params).fetchall()

    def recent_recipes(self, user_id, limit=5):
        with self.connect() as conn:
            return conn.execute(
                "SELECT * FROM recipes WHERE user_id=? ORDER BY datetime(created_at) DESC LIMIT ?",
                (user_id, limit),
            ).fetchall()

    def set_saved(self, recipe_id, user_id, value):
        with self.connect() as conn:
            conn.execute("UPDATE recipes SET is_saved=? WHERE id=? AND user_id=?", (int(value), recipe_id, user_id))

    def set_favorite(self, recipe_id, user_id, value):
        with self.connect() as conn:
            conn.execute("UPDATE recipes SET is_favorite=? WHERE id=? AND user_id=?", (int(value), recipe_id, user_id))

    def delete_recipe(self, recipe_id, user_id):
        with self.connect() as conn:
            conn.execute("DELETE FROM recipes WHERE id=? AND user_id=?", (recipe_id, user_id))

    def clear_history(self, user_id):
        with self.connect() as conn:
            conn.execute("DELETE FROM recipes WHERE user_id=? AND is_saved=0", (user_id,))

    def stats(self, user_id):
        with self.connect() as conn:
            row = conn.execute("""
                SELECT
                    COUNT(*) total,
                    COALESCE(SUM(is_saved), 0) saved,
                    COALESCE(SUM(is_favorite), 0) favorites
                FROM recipes WHERE user_id=?
            """, (user_id,)).fetchone()
            return dict(row)
