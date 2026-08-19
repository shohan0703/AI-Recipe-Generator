import json
from pathlib import Path

from config import ASSETS_DIR


def recipe_from_row(row):
    data = dict(row)
    data["ingredients"] = json.loads(data.get("ingredients") or "[]")
    data["instructions"] = json.loads(data.get("instructions") or "[]")
    data["cooking_tips"] = json.loads(data.get("cooking_tips") or "[]")
    return data


def choose_image(recipe_name: str, cuisine: str = "") -> str:
    name = f"{recipe_name} {cuisine}".lower()
    candidates = [
        ("chicken", "biryani.jpg"),
        ("biryani", "biryani.jpg"),
        ("rice", "biryani.jpg"),
        ("curry", "biryani.jpg"),
        ("pasta", "combo_meal.jpg"),
        ("noodle", "combo_meal.jpg"),
        ("salad", "ingredients.jpg"),
        ("vegetable", "ingredients.jpg"),
        ("dessert", "combo_meal.jpg"),
    ]
    for key, filename in candidates:
        path = ASSETS_DIR / filename
        if key in name and path.exists():
            return str(path)
    for filename in ("combo_meal.jpg", "biryani.jpg", "default_food.png"):
        path = ASSETS_DIR / filename
        if path.exists():
            return str(path)
    return ""
